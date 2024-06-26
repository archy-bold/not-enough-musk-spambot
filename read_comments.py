#!/usr/bin/env python3
import argparse
import os
import sys
from typing import List
import praw
import sqlite3 as sl
from src.db import get_replied_comment_ids, get_replied_submission_ids
from src.env import load_env_from_flags, read_env
from src.reddit import bot_login
from src.stats.db import have_comment, insert_comment, update_comment
from src.gcs import *

parser = argparse.ArgumentParser()
parser.add_argument("mode", choices = ["latest", "historic"], default = None, help="Whether to load reacent or historic comments")
load_env_from_flags(parser)

gcs_bucket: str = read_env('GCS_BUCKET', None)
gcs_key: str = read_env('GCS_KEY', secret=True, default=None)

doLatest: bool = parser.parse_args().mode == "latest"

r: praw.Reddit = bot_login()
me: any = r.user.me(use_cache=True)
dir: str = os.path.dirname(os.path.realpath(__file__))

# Get the stats database from GCS
download_db_file_from_gcs(gcs_bucket, gcs_key, dir, 'stats.db')
if not doLatest:
    download_db_file_from_gcs(gcs_bucket, gcs_key, dir, 'bot.db')

# Read the stats database
conStats: sl.Connection = sl.connect(dir + '/stats.db')
cStats: sl.Cursor = conStats.cursor()

count_inserted: int = 0
count_updated: int = 0
if doLatest:
    # read all comments from reddit user
    for comment in me.comments.new(limit=None):
        if not have_comment(cStats, comment.id):
            count_inserted += 1
            insert_comment(cStats, comment)
        else:
            count_updated += 1
            update_comment(cStats, comment)
    print("Inserted " + str(count_inserted) + " comments")
    print("Updated " + str(count_updated) + " comments")

else:
    # Read the bot database
    conBot: sl.Connection = sl.connect(dir + '/bot.db')
    cBot: sl.Cursor = conBot.cursor()

    submissions: List[str] = get_replied_submission_ids(cBot)
    comments: List[str] = get_replied_comment_ids(cBot)

    conBot.close()

    # For every replied submission, find our reply and get its stats
    for submission_id in submissions:
        submission: any = r.submission(id=submission_id)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            if comment.author == me:
                print("Found comment \"" + comment.id + "\" in submission \"" + submission.id + "\"")
                if not have_comment(cStats, comment.id):
                    insert_comment(cStats, comment)
                else:
                    update_comment(cStats, comment)
                break
    conStats.commit()

    # For every replied comment, find our reply and get its stats
    commentCount = len(comments)
    i = 0
    for comment_id in comments:
        comment: any = r.comment(id=comment_id)
        comment.refresh()
        try:
            comment.replies.replace_more(limit=None)
            comment.replies.replace_more(limit=None)
            comment.replies.replace_more(limit=None)
        except praw.exceptions.PRAWException as e:
            print("Failed to replace more for comment \"" + comment.id + "\" (" + str(i) + "/" + str(commentCount) + ")")
        for reply in comment.replies.list():
            if isinstance(reply, praw.models.MoreComments):
                print("Found MoreComments object on comment \"" + comment.id + "\" (" + str(i) + "/" + str(commentCount) + ")")
                continue
            if reply.author == me:
                # print("Found reply \"" + reply.id + "\" to comment \"" + comment.id + "\"")
                if not have_comment(cStats, reply.id):
                    insert_comment(cStats, reply)
                else:
                    update_comment(cStats, reply)
                break
        i += 1

conStats.commit()
upload_db_file_to_gcs(gcs_bucket, gcs_key, dir, 'stats.db')
