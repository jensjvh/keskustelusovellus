"""A module for handling functionalities related to topics."""

from db import db
from sqlalchemy import text
from datetime import datetime


def get_topics():
    """
    Get all existing topics. Convert the created time to readable format.
    """
    sql = text("""
        SELECT T.title AS title, T.text_id AS text_id,
               COUNT(DISTINCT Th.id) AS threads,
               COUNT(R.id) AS replies,
               MAX(R.created_time) AS last_reply
        FROM Topics T
        LEFT JOIN Threads Th ON T.id = Th.topic_id
        LEFT JOIN Replies R ON Th.id = R.thread_id
        GROUP BY T.id
        ORDER BY T.title;
    """)
    result = db.session.execute(sql)

    topics = result.fetchall()

    formatted_topics = []

    for topic in topics:
        new_topic = {'title': topic.title,
                     'text_id': topic.text_id,
                     'threads': topic.threads,
                     'replies': topic.replies
                     }
        if topic.last_reply:
            new_topic['last_reply'] = topic.last_reply.strftime("%Y.%m.%d %H:%M:%S")
        else:
            new_topic['last_reply'] = 'No replies'

        formatted_topics.append(new_topic)

    return formatted_topics


def get_topic_by_title(title):
    """
    Function for returning the SQL query result of topic with given title.
    """
    sql = text("""
        SELECT id, text_id, title, description, is_hidden
        FROM Topics WHERE title = :title;
    """)
    result = db.session.execute(sql, {"title": title})

    return result.fetchone()


def get_topic_by_text_id(text_id):
    """
    Function for returning the SQL query result of topic with given text id.
    """
    sql = text("""
        SELECT id, text_id, title, description, is_hidden
        FROM Topics WHERE text_id = :text_id
    """)
    result = db.session.execute(sql, {"text_id": text_id})

    return result.fetchone()
