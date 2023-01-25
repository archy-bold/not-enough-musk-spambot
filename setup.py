import sqlite3 as sl

con = sl.connect('bot.db')

with con:
    con.execute("""
        CREATE TABLE comments (
            id VARCHAR(50) NOT NULL PRIMARY KEY,
            submission_id VARCHAR(50),
            subreddit VARCHAR(50),
            replied BOOLEAN,
            score INTEGER
        );
    """)
    con.execute("""
        CREATE TABLE submissions (
            id VARCHAR(50) NOT NULL PRIMARY KEY,
            subreddit VARCHAR(50),
            replied BOOLEAN,
            score INTEGER
        );
    """)
