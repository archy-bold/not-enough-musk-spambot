#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import praw
import time
import os
import random
import sqlite3 as sl
import sys
import traceback
from dotenv import load_dotenv

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
submission_replies = {
    "tesla": [
        "We don’t control the federal reserve. The higher the rates, the harder they fall",
        "The fun police made us do it (sigh)"],
    "files": ["!!", "Interesting"],
    "twitter": [
        "Looking into this.",
        "Looking into this.",
        "Looking into this.",
        "Interesting",
        "Interesting",
        "Interesting",
        "Something fundamental is wrong",
        "Something is wrong"],
    " bot": [
        "Looking into this.",
        "Looking into this.",
        "Looking into this.",
        "Interesting",
        "Interesting",
        "Interesting",
        "Something fundamental is wrong",
        "Something is wrong",
        "Just ~$100/month for API access with ID verification will clean things up greatly."],
    "no plan": ["Amazing. You're a jackass!"],
    "wealth": ["I’m rich, bitch!"],
    "fascism": ["Comedy is now legal on Twitter.", "Interesting"],
    "fascist": ["Comedy is now legal on Twitter."],
    "severance": ["You’re fired."],
    "engineer": ["Print out 50 pages of code you’ve done in the last 30 days"],
    "takeover": ["Let that sink in"],
}

comment_replies = {
    "crypto": ["I will keep supporting Dogecoin"],
    "dogecoin": ["I will keep supporting Dogecoin"],
    "spacex": [
        "My car is orbiting mars",
        "Humanity will reach Mars in 2026",
        "Unless it is stopped, the woke mind virus will destroy civilization and humanity will never reach Mars"],
    "stephen king": ["I’m still a fan tbh"],
    "mastadon": ["What do you call someone who is a master at baiting?"],
    "mastodon": ["What do you call someone who is a master at baiting?"],
    "files": ["!!", "Interesting"],
    "twitter blue": ["We need to pay the bills somehow! How about $20?"],
    "twitter": [
        "Pay me $8!",
        "Pay me $8!",
        "Pay me $8!",
        "Looking into this.",
        "Looking into this.",
        "Looking into this.",
        "Interesting",
        "Interesting",
        "Interesting",
        "Something fundamental is wrong",
        "Something is wrong"],
    "king of twitter": ["Let that sink in"],
    "dad joke": ["Let that sink in"],
    "takeover": ["Let that sink in"],
    "engineer": ["Print out 50 pages of code you’ve done in the last 30 days"],
    "developer": [
        "Print out 50 pages of code you’ve done in the last 30 days",
        "Just ~$100/month for API access with ID verification will clean things up greatly."],
    "server": ["Print out 50 pages of code you’ve done in the last 30 days"],
    "severance": ["You’re fired."],
    "employee": ["You’re fired.", "We’re going to need you to stay in overnight, we’re going ultra hardcore."],
    "fired": ["You’re fired!"],
    "working hours": ["Are you super hardcore?", "Are you extremely hardcore?"],
    "hardcore": ["Are you super hardcore?", "Are you extremely hardcore?"],
    "covid": ["My pronouns are Prosecute/Fauci", "The coronavirus pandemic is dumb."],
    "daughter": ["Can’t win ‘em all"],
    "thai": ["Such a pedo guy"],
    "wealth": ["I’m rich, bitch!"],
    "stock": ["Funding secured."],
    "loan": ["Funding secured."],
    "interest rate": ["Funding secured.", "Interesting"],
    "republican": ["I’m not right wing.", "Interesting"],
    " ban ": ["Comedy is now legal on Twitter."],
    " bans": ["Comedy is now legal on Twitter."],
    "suspend": ["Comedy is now legal on Twitter."],
    "fascism": ["Comedy is now legal on Twitter.", "Interesting"],
    "fascist": ["Comedy is now legal on Twitter.", "Interesting"],
    "resign": ["I will resign as CEO as soon as I find someone foolish enough to take the job! After that, I will just run the software & servers teams."],
    "woke": [
        "The woke mind virus is either defeated or nothing else matters",
        "Unless it is stopped, the woke mind virus will destroy civilization and humanity will never reach Mars"],
    "pronouns": [
        "My pronouns are Prosecute/Fauci",
        "Pronouns suck",
        "The woke mind virus is either defeated or nothing else matters"],
    "chappelle": ["What do I say, Dave?"],
    "neuralink": ["We are now confident that the Neuralink device is ready for humans"],
    "batchnorm": ["Gaming rocks"],
    "game": ["Gaming rocks"],
    # "trans": ["My pronouns are Prosecute/Fauci", "Pronouns suck"],
    # boring company
    # microservices just add bloat
}

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
                if key in submission.title.lower() and submission.author != me:
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
                if key in comment.body.lower() and comment.author != me:
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
