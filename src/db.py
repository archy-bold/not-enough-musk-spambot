#!/usr/bin/env python3
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

def have_replied_to_submission(c: sl.Cursor, id: str) -> Optional[bool]:
    # Get the submission from the db
    run_query(c, 'SELECT replied FROM submissions WHERE id= ?', (id,))
    res: Optional[List[bool]] = c.fetchone()
    if res is None:
        return None
    else:
        return bool(res[0])

def have_replied_to_comment(c: sl.Cursor, id: str) -> Optional[bool]:
    # Get the comment from the cb
    run_query(c, 'SELECT replied FROM comments WHERE id= ?', (id,))
    res: Optional[List[bool]] = c.fetchone()
    if res is None:
        return None
    else:
        return bool(res[0])

def insert_submission(c: sl.Cursor, submission: any, replied: bool =True) -> None:
    run_query(
        c,
        'INSERT INTO submissions (id, subreddit, score, replied) VALUES (?, ?, ?, ?)',
        (submission.id, submission.subreddit.display_name, submission.score, replied,))

def insert_comment(c: sl.Cursor, comment: any, replied: bool =True) -> None:
    run_query(
        c,
        'INSERT INTO comments (id, submission_id, subreddit, score, replied) VALUES (?, ?, ?, ?, ?)',
        (comment.id, comment.submission.id, comment.subreddit.display_name, comment.score, replied,))

def get_replied_comment_ids(c: sl.Cursor) -> List[str]:
    run_query(c, 'SELECT id FROM comments WHERE replied=1')
    return [row[0] for row in c.fetchall()]

def get_replied_submission_ids(c: sl.Cursor) -> List[str]:
    run_query(c, 'SELECT id FROM submissions WHERE replied=1')
    return [row[0] for row in c.fetchall()]
