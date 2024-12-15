"""A module for handling functionalities related to topics."""
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from flask import flash


from db import db


MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 25
MIN_TEXT_ID_LENGTH = 1
MAX_TEXT_ID_LENGTH = 25
MIN_DESC_LENGTH = 1
MAX_DESC_LENGTH = 50
VALID_TEXT_ID_CHARACTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.~"


def validate_topic(title, text_id, description):
    """Validate the parameters for a topic."""
    if not validate_title(title):
        flash("Invalid title length", "error")
        return False
    if not validate_text_id(text_id):
        flash("Invalid text id characters or length", "error")
        return False
    if not validate_description(description):
        flash("Invalid description", "error")
        return False
    return True


def validate_title(title):
    """Validate a title's length."""
    if len(title) > MAX_TITLE_LENGTH or len(title) < MIN_TITLE_LENGTH:
        return False
    return True


def validate_text_id(text_id):
    """Validate a topic text id length and characters."""
    if len(text_id) > MAX_TEXT_ID_LENGTH or len(text_id) < MIN_TITLE_LENGTH:
        return False
    for c in text_id:
        if c not in VALID_TEXT_ID_CHARACTERS:
            flash(c, VALID_TEXT_ID_CHARACTERS)
            return False
    return True


def validate_description(description):
    """Validate a topic description length."""
    if len(description) > MAX_DESC_LENGTH or len(description) < MIN_DESC_LENGTH:
        return False
    return True


def create_topic(text_id, title, description, is_hidden=False):
    """
    Create a new topic.
    """
    try:
        sql = text(
            """INSERT INTO topics (text_id, title, description, is_hidden)
                    VALUES (:text_id, :title, :description, :is_hidden);"""
        )
        db.session.execute(sql, {"text_id": text_id,
                                 "title": title,
                                 "description": description,
                                 "is_hidden": is_hidden})
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True


def edit_topic_with_topic_id(topic_id, text_id, title, description, is_hidden):
    """
    A function for changing the text id, title, 
    description, and hiding of a topic.
    """
    try:
        sql = text("""
                UPDATE topics
                SET text_id = :text_id,
                title = :title,
                description = :description,
                is_hidden = :is_hidden
                WHERE id = :topic_id;
                """)
        db.session.execute(sql, {"topic_id": topic_id,
                                 "text_id": text_id,
                                 "title": title,
                                 "description": description,
                                 "is_hidden": is_hidden})
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return True


def remove_topic_with_topic_id(topic_id):
    """
    Remove a topic with given id.
    """
    sql = text("""
               DELETE FROM topics
               WHERE id = :topic_id;
               """)

    db.session.execute(sql, {"topic_id": topic_id})

    db.session.commit()


def get_visible_topics():
    """
    Get all visible topics. Convert the created time to readable format.
    """
    sql = text("""
        SELECT T.title AS title, T.text_id AS text_id,
               COUNT(DISTINCT Th.id) AS threads,
               COUNT(R.id) AS replies,
               MAX(R.created_time) AS last_reply
        FROM Topics T
        LEFT JOIN Threads Th ON T.id = Th.topic_id
        LEFT JOIN Replies R ON Th.id = R.thread_id
        WHERE T.is_hidden = FALSE
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
            new_topic['last_reply'] = topic.last_reply.strftime(
                "%Y.%m.%d %H:%M:%S")
        else:
            new_topic['last_reply'] = 'No replies'

        formatted_topics.append(new_topic)

    return formatted_topics


def get_all_topics():
    """
    Get all topics, including hidden ones. Convert the created time to readable format.
    """
    sql = text("""
        SELECT T.title AS title, T.text_id AS text_id,
               COUNT(DISTINCT Th.id) AS threads,
               COUNT(R.id) AS replies,
               MAX(R.created_time) AS last_reply,
               T.is_hidden AS is_hidden
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
                     'replies': topic.replies,
                     'is_hidden': topic.is_hidden
                     }
        if topic.last_reply:
            new_topic['last_reply'] = topic.last_reply.strftime(
                "%Y.%m.%d %H:%M:%S")
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


def get_topic_by_id(topic_id):
    """
    Function for returning the SQL query result of topic with given id.
    """
    sql = text("""
        SELECT id, text_id, title, description, is_hidden
        FROM Topics WHERE id = :topic_id;
    """)
    result = db.session.execute(sql, {"topic_id": topic_id})

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
