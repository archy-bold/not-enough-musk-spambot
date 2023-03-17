#!/usr/bin/env python3
import praw
import time
import os
import random
import sqlite3 as sl
import sys
import traceback
from dotenv import load_dotenv
from typing import Optional, List
from phrases import *

load_dotenv()

subreddit: str = os.getenv('SUBREDDIT')
sleep: int = int(os.getenv('SLEEP'))
submission_prob: float = float(os.getenv('SUBMISSION_PROBABILITY'))
comment_prob: float = float(os.getenv('COMMENT_PROBABILITY'))
env: str = os.getenv('ENV', 'test')
mode: str = os.getenv('MODE', 'once')
reply_age: int = int(os.getenv('REPLY_AGE', 7))
me = None
print("SUBREDDIT=" + subreddit)
print("SLEEP=" + str(sleep) + "s")
print("SUBMISSION_PROBABILITY=" + str(submission_prob * 100) + "%")
print("COMMENT_PROBABILITY=" + str(comment_prob * 100) + "%")
print("ENV=" + env)
print("MODE=" + mode)
print("REPLY_AGE=" + str(reply_age))

def bot_login() -> praw.Reddit:
    print("Logging in...")
    username: str = os.getenv('BOT_NAME')
    password: str = os.getenv('PASSWORD')
    client_id: str = os.getenv('CLIENT_ID')
    client_secret: str = os.getenv('CLIENT_SECRET')
    r: praw.Reddit = praw.Reddit(username = username,
                password = password,
                client_id = client_id,
                client_secret = client_secret,
                user_agent = "r/EnoughMuskSpam bot")
    print("Logged in as " + str(r.user.me()))

    return r

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

    print("Search Completed.")

    if env != "production":
        con.commit()

    print("Sleeping for " + str(sleep) + " seconds...")
    time.sleep(sleep)

def have_replied_to_submission(c: sl.Cursor, id: str) -> Optional[bool]:
    # Get the submission from the db
    c.execute('SELECT replied FROM submissions WHERE id= ?', (id,))
    res: Optional[List[bool]] = c.fetchone()
    if res is None:
        return None
    else:
        return bool(res[0])

def have_replied_to_comment(c: sl.Cursor, id: str) -> Optional[bool]:
    # Get the comment from the cb
    c.execute('SELECT replied FROM comments WHERE id= ?', (id,))
    res: Optional[List[bool]] = c.fetchone()
    if res is None:
        return None
    else:
        return bool(res[0])

def insert_submission(c: sl.Cursor, submission: any, replied: bool =True) -> None:
    try:
        c.execute(
            'INSERT INTO submissions (id, subreddit, score, replied) VALUES (?, ?, ?, ?)',
            (submission.id, submission.subreddit.display_name, submission.score, replied,))
    except sl.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

def insert_comment(c: sl.Cursor, comment: any, replied: bool =True) -> None:
    try:
        c.execute(
            'INSERT INTO comments (id, submission_id, subreddit, score, replied) VALUES (?, ?, ?, ?, ?)',
            (comment.id, comment.submission.id, comment.subreddit.display_name, comment.score, replied,))
    except sl.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

def text_contains(haystack: str, needle: str) -> bool:
    return needle in haystack.lower() or (needle.endswith("$") and haystack.lower().endswith(needle.replace("$", "")))

def timestamp_older_than_days(ts: float, days: int) -> bool:
    return (time.time() - ts) > (days * 86400)

r: praw.Reddit = bot_login()
me: any = r.user.me(use_cache=True)
dir: str = os.path.dirname(os.path.realpath(__file__))
con: sl.Connection = sl.connect(dir + '/bot.db')
c: sl.Cursor = con.cursor()

if mode == "once":
    run_bot(r, con, c)
else:
    while True:
        run_bot(r, con, c)
