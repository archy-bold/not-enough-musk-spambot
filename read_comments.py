#!/usr/bin/env python3
import os
import sys
from typing import List
import praw
import sqlite3 as sl
from src.db import get_replied_comment_ids, get_replied_submission_ids
from src.reddit import bot_login
from src.stats.db import have_comment, insert_comment, update_comment

# read argument 
if len(sys.argv) != 2:
    print("Usage: python3 read_comments.py <latest | historic>")
    sys.exit(1)

doLatest: bool = sys.argv[1] == "latest"

r: praw.Reddit = bot_login()
me: any = r.user.me(use_cache=True)
dir: str = os.path.dirname(os.path.realpath(__file__))

# Read the stats database
conStats: sl.Connection = sl.connect(dir + '/stats.db')
cStats: sl.Cursor = conStats.cursor()

if doLatest:
    # read all comments from reddit user
    for comment in me.comments.hot(limit=None):
        if not have_comment(cStats, comment.id):
            insert_comment(cStats, comment)

else:
    # Read the bot database
    conBot: sl.Connection = sl.connect(dir + '/live.db')
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
