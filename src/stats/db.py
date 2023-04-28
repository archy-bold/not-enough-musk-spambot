#!/usr/bin/env python3
import datetime
import sqlite3 as sl
import sys
import traceback
from typing import Optional, List
    
def run_query(c: sl.Cursor, query: str, params: tuple = ()) -> None:
    try:
        c.execute(query, params)
    except sl.Error as er:
        print('SQLite error: %s' % (' '.join(er.args)))
        print("Exception class is: ", er.__class__)
        print('SQLite traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

def insert_comment(c: sl.Cursor, comment: any) -> None:
    run_query(
        c,
        'INSERT INTO comments (id, submission_id, parent_id, subreddit, body, permalink, score, commented_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (
            comment.id,
            comment.submission.id,
            comment.parent_id,
            comment.subreddit.display_name,
            comment.body,
            comment.permalink,
            comment.score,
            datetime.datetime.fromtimestamp(comment.created_utc)))
    
def update_comment(c: sl.Cursor, comment: any) -> None:
    run_query(
        c,
        'UPDATE comments SET body=?, score=? WHERE id=?',
        (comment.body, comment.score, comment.id,))

def have_comment(c: sl.Cursor, id: str) -> bool:
    # Get the comment from the cb
    run_query(c, 'SELECT id FROM comments WHERE id= ?', (id,))
    res: Optional[List[bool]] = c.fetchone()
    if res is None:
        return False
    else:
        return True
