import praw
import time
import os
import sqlite3 as sl
import sys
import traceback
from dotenv import load_dotenv

load_dotenv()

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
                user_agent = "testscript by u/archy_bold")
    print("Logged in!")
    print(r.user.me())

    return r

def run_bot(r, con, c):

    print("Searching newest submissions")
    for submission in r.subreddit('test').new():
        replied = have_replied_to_submission(c, submission.id)
        if replied is None:
            if "musk" in submission.title and submission.author != r.user.me():
                print("String with \"musk\" found in submission " + submission.title + " " + submission.id)
                submission.reply("Interesting")
                print("Replied to submission " + submission.id)

                insert_submission(c, submission)

    print("Search Completed.")

    print("Searching last 1,000 comments")
    for comment in r.subreddit('test').comments(limit=1000):
        replied = have_replied_to_comment(c, comment.id)
        if replied is None:
            if "interesting" in comment.body and comment.author != r.user.me():
                print("String with \"interesting\" found in comment \"" + comment.body + "\" " + comment.id)
                comment.reply("!!")
                print("Replied to comment " + comment.id)

                insert_comment(c, comment)

    print("Search Completed.")

    con.commit()

    print("Sleeping for 10 seconds...")
    #Sleep for 10 seconds...		
    time.sleep(10)

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
            'INSERT INTO submissions (id, subreddit, replied) VALUES (?, ?, ?)',
            (submission.id, submission.subreddit.display_name, replied,))
    except sl.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

def insert_comment(c, comment, replied =True):
    try:
        c.execute(
            'INSERT INTO comments (id, submission_id, subreddit, replied) VALUES (?, ?, ?, ?)',
            (comment.id, comment.submission.id, comment.subreddit.display_name, replied,))
    except sl.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))


r = bot_login()
con = sl.connect('bot.db')
c = con.cursor()

while True:
    run_bot(r, con, c)
