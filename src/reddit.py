#!/usr/bin/env python3
import praw
from src.env import read_env

def bot_login() -> praw.Reddit:
    print("Logging in...")
    username: str = read_env('BOT_NAME')
    password: str = read_env('PASSWORD')
    client_id: str = read_env('CLIENT_ID')
    client_secret: str = read_env('CLIENT_SECRET')
    r: praw.Reddit = praw.Reddit(username = username,
                password = password,
                client_id = client_id,
                client_secret = client_secret,
                user_agent = "r/EnoughMuskSpam bot")
    print("Logged in as " + str(r.user.me()))

    return r
