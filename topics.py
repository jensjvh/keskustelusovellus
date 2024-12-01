from db import db
from sqlalchemy import text


def get_topics():
    sql = text("""
        SELECT T.title AS title, T.text_id AS text_id,
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

def get_topic_by_title(title):
    sql = text("""
        SELECT * FROM Topics WHERE title = ':title'
    """)
    result = db.session.execute(sql, {"title": title})

    return result.fetchone()

def get_topic_by_text_id(text_id):
    sql = text("""
        SELECT * FROM Topics WHERE text_id = :text_id
    """)
    result = db.session.execute(sql, {"text_id": text_id})

    return result.fetchone()