#!/usr/bin/env python3
import praw
import time
import os
import random
import sqlite3 as sl
from phrases import *
from prawcore.exceptions import ServerError
from src.db import *
from src.env import *
from src.reddit import *
from src.gcs import *

load_env_from_flags()

subreddit: str = read_env('SUBREDDIT')
sleep: int = read_env_int('SLEEP')
submission_prob: float = read_env_float('SUBMISSION_PROBABILITY')
comment_prob: float = read_env_float('COMMENT_PROBABILITY')
env: str = read_env('ENV', 'test')
mode: str = read_env('MODE', 'once')
reply_age: int = read_env_int('REPLY_AGE', 7)
gcs_bucket: str = read_env('GCS_BUCKET', None)
gcs_key: str = read_env('GCS_KEY', secret=True, default=None)
me = None

def run_bot(r: praw.Reddit, con: sl.Connection, c: sl.Cursor) -> None:

    print("Searching newest submissions")
    for submission in r.subreddit(subreddit).new():
        replied = have_replied_to_submission(c, submission.id)
        if replied is None:
            for key in submission_replies:
                if (text_contains(submission.title, key) and
                    submission.author != me and
                        not submission.locked and
                            not timestamp_older_than_days(submission.created_utc, reply_age)):
                    print("String with \"" + key + "\" found in submission " + submission.title + " " + submission.id)
                    if random.random() < submission_prob:
                        response: str = random.choice(submission_replies[key])
                        if env == "production":
                            submission.reply(response)
                            time.sleep(2)
                        print("Replied to submission \"" + submission.id + "\" with \"" + response + "\"")

                        insert_submission(c, submission, replied=True)
                    else:
                        insert_submission(c, submission, replied=False)

                    if env == "production":
                        con.commit()
                    break

    print("Search Completed.")

    print("Searching last 1,000 comments")
    for comment in r.subreddit(subreddit).comments(limit=1000):
        replied = have_replied_to_comment(c, comment.id)
        if replied is None:
            for key in comment_replies:
                try:
                    if (text_contains(comment.body, key) and
                            comment.author != me and
                                not comment.submission.locked and
                                    not timestamp_older_than_days(comment.created_utc, reply_age)):
                        print("String with \"" + key + "\" found in comment \"" + comment.body + "\" " + comment.id + " (submission " + comment.submission.id + ")")
                        if random.random() < comment_prob:
                            response: str = random.choice(comment_replies[key])
                            if response.lower() in comment.body.lower():
                                break

                            if env == "production":
                                comment.reply(response)
                                con.commit()
                                time.sleep(2)
                            print("Replied to comment \"" + comment.id + "\" with \"" + response + "\"")

                            insert_comment(c, comment, replied=True)
                        else:
                            insert_comment(c, comment, replied=False)

                        if env == "production":
                            con.commit()
                        break
                except ServerError as e:
                    # 504 gateway timeouts seem to happen when accessing submissions unavailable to the bot, ignore them
                    # eg seen when accessing the submission of comment jxl3ied (sub id 15zi1up)
                    if e.response.status_code != 504:
                        raise
                except praw.exceptions.RedditAPIException as e:
                    # Do nothing, don't reply to deleted comments.
                    print("Don't reply to deleted comment " + comment.id + " \"" + comment.body + "\"")

    print("Search Completed.")

    if env != "production":
        con.commit()

    print("Sleeping for " + str(sleep) + " seconds...")
    time.sleep(sleep)

def text_contains(haystack: str, needle: str) -> bool:
    return needle in haystack.lower() or (needle.endswith("$") and haystack.lower().endswith(needle.replace("$", "")))

def timestamp_older_than_days(ts: float, days: int) -> bool:
    return (time.time() - ts) > (days * 86400)

# Load reddit
r: praw.Reddit = bot_login()
me: any = r.user.me(use_cache=True)

# Load the DB
dir: str = os.path.dirname(os.path.realpath(__file__))
# Check GCS if we have a GCS key
gcs_client: storage.Client = None
if gcs_bucket is not None and gcs_key is not None:
    gcs_client = get_gcs_client(gcs_key)
    gcs_client.bucket(gcs_bucket).get_blob('bot.db').download_to_filename(dir + '/bot.db')

con: sl.Connection = sl.connect(dir + '/bot.db')
c: sl.Cursor = con.cursor()

if mode == "once":
    run_bot(r, con, c)
    if gcs_client is not None:
        gcs_client.bucket(gcs_bucket).blob('bot.db').upload_from_filename(dir + '/bot.db')
else:
    while True:
        run_bot(r, con, c)
        gcs_client.bucket(gcs_bucket).blob('bot.db').upload_from_filename(dir + '/bot.db')
