#!/usr/bin/env python3
import praw
import time
import os
import random
import sqlite3 as sl
import sys
import traceback
from dotenv import load_dotenv
from phrases import *

load_dotenv()

subreddit = os.getenv('SUBREDDIT')
sleep = int(os.getenv('SLEEP'))
submission_prob = float(os.getenv('SUBMISSION_PROBABILITY'))
comment_prob = float(os.getenv('COMMENT_PROBABILITY'))
env = os.getenv('ENV', 'test')
mode = os.getenv('MODE', 'once')
me = None
print("SUBREDDIT=" + subreddit)
print("SLEEP=" + str(sleep) + "s")
print("SUBMISSION_PROBABILITY=" + str(submission_prob * 100) + "%")
print("COMMENT_PROBABILITY=" + str(comment_prob * 100) + "%")
print("ENV=" + env)
print("MODE=" + mode)

def bot_login():
    print("Logging in...")
    username = os.getenv('BOT_NAME')
    password = os.getenv('PASSWORD')
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    r = praw.Reddit(username = username,
                password = password,
                client_id = client_id,
                client_secret = client_secret,
                user_agent = "r/EnoughMuskSpam bot")
    print("Logged in as " + str(r.user.me()))

    return r

def run_bot(r, con, c):

    print("Searching newest submissions")
    for submission in r.subreddit(subreddit).new():
        replied = have_replied_to_submission(c, submission.id)
        if replied is None:
            for key in submission_replies:
                if text_contains(submission.title, key) and submission.author != me:
                    print("String with \"" + key + "\" found in submission " + submission.title + " " + submission.id)
                    if random.random() < submission_prob:
                        response = random.choice(submission_replies[key])
                        if env == "production":
                            submission.reply(response)
                            time.sleep(2)
                        print("Replied to submission " + submission.id + " with " + response)

                        insert_submission(c, submission, replied=True)
                    else:
                        insert_submission(c, submission, replied=False)

                    if env == "production":
                        con.commit()
                    break

    print("Search Completed.")

    print("Searching last 1,000 comments")
    for comment in r.subreddit('EnoughMuskSpam').comments(limit=1000):
        replied = have_replied_to_comment(c, comment.id)
        if replied is None:
            for key in comment_replies:
                if text_contains(comment.body, key) and comment.author != me:
                    print("String with \"" + key + "\" found in comment \"" + comment.body + "\" " + comment.id)
                    if random.random() < comment_prob:
                        response = random.choice(comment_replies[key])
                        if env == "production":
                            comment.reply(response)
                            con.commit()
                            time.sleep(2)
                        print("Replied to comment " + comment.id + " with " + response)

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

def have_replied_to_submission(c, id):
    # Get the submission from the db
    c.execute('SELECT replied FROM submissions WHERE id= ?', (id,))
    res = c.fetchone()
    if res is None:
        return None
    else:
        return bool(res[0])

def have_replied_to_comment(c, id):
    # Get the comment from the cb
    c.execute('SELECT replied FROM comments WHERE id= ?', (id,))
    res = c.fetchone()
    if res is None:
        return None
    else:
        return bool(res[0])

def insert_submission(c, submission, replied =True):
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

def insert_comment(c, comment, replied =True):
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

def text_contains(haystack, needle):
    return needle in haystack.lower() or (needle.endswith("$") and haystack.lower().endswith(needle.replace("$", "")))

r = bot_login()
me = r.user.me(use_cache=True)
dir = os.path.dirname(os.path.realpath(__file__))
con = sl.connect(dir + '/bot.db')
c = con.cursor()

if mode == "once":
    run_bot(r, con, c)
else:
    while True:
        run_bot(r, con, c)
