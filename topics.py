from flask import request, session
from db import db
from sqlalchemy import text


def get_topics():
    sql = text("""
        SELECT T.title AS title,
               COUNT(Th.id) AS threads,
               COUNT(R.id) AS replies,
               COALESCE(MAX(R.created_time)::TEXT, 'No replies') AS last_reply
        FROM Topics T
        LEFT JOIN Threads Th ON T.id = Th.topic_id
        LEFT JOIN Replies R ON Th.id = R.thread_id
        GROUP BY T.id;
    """)
    result = db.session.execute(sql)

    return result.fetchall()
