import sqlite3 as sl

con = sl.connect('stats.db')

with con:
    con.execute("""
        CREATE TABLE comments (
            id VARCHAR(50) NOT NULL PRIMARY KEY,
            submission_id VARCHAR(50),
            parent_id VARCHAR(50),
            subreddit VARCHAR(50),
            body TEXT,
            permalink VARCHAR(100),
            score INTEGER,
            commented_at DATETIME
        );
    """)
