import praw
import time
import os
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

def run_bot(r, submissions_replied_to, comments_replied_to):

    print("Searching newest submissions")
    for submission in r.subreddit('test').new():
        if "musk" in submission.title and submission.id not in submissions_replied_to and submission.author != r.user.me():
            print("String with \"musk\" found in submission " + submission.id)
            submission.reply("Interesting")
            print("Replied to submission " + submission.id)
            submissions_replied_to.append(submission.id)

            with open ("submissions_replied_to.txt", "a") as f:
                f.write(submission.id + "\n")

    print("Search Completed.")

    print(submissions_replied_to)

    print("Searching last 1,000 comments")
    for comment in r.subreddit('test').comments(limit=1000):
        if "interesting" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
            print("String with \"interesting\" found in comment " + comment.id)
            comment.reply("!!")
            print("Replied to comment " + comment.id)

            comments_replied_to.append(comment.id)

            with open ("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

    print("Search Completed.")

    print(comments_replied_to)

    print("Sleeping for 10 seconds...")
    #Sleep for 10 seconds...		
    time.sleep(10)

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
            comments_replied_to = list(filter(None, comments_replied_to))

    return comments_replied_to

def get_saved_submissions():
    if not os.path.isfile("submissions_replied_to.txt"):
        submissions_replied_to = []
    else:
        with open("submissions_replied_to.txt", "r") as f:
            submissions_replied_to = f.read()
            submissions_replied_to = submissions_replied_to.split("\n")
            submissions_replied_to = list(filter(None, submissions_replied_to))

    return submissions_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
submissions_replied_to = get_saved_submissions()
print(comments_replied_to)
print(submissions_replied_to)

while True:
    run_bot(r, submissions_replied_to, comments_replied_to)
