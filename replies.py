"""A module for handling functionalities related to replies."""

from sqlalchemy import text
from db import db


def get_replies(thread_id):
    """Get replies from a specific thread."""
    sql = text("""
            SELECT R.id as id,
                   U.username as username,
                   R.content as content,
                   R.created_time as created_time
            FROM replies R
            INNER JOIN threads Th ON Th.id = R.thread_id
            INNER JOIN users U on R.user_id = U.id
            WHERE R.thread_id = :thread_id
            ORDER BY R.created_time ASC;""")

    result = db.session.execute(sql, {"thread_id": thread_id})

    replies = result.fetchall()

    formatted_replies = format_replies(replies)

    return formatted_replies

def get_matching_replies(query):
    """Get replies matching a pattern."""
    sql = text("""
        SELECT R.id as id,
               U.username as username,
               R.content as content,
               R.created_time as created_time,
               Th.title as thread_title,
               Th.id as thread_id,
               T.title as topic_title,
               T.text_id as topic_text_id
        FROM replies R
        INNER JOIN users U on R.user_id = U.id
        INNER JOIN threads Th on R.thread_id = Th.id
        INNER JOIN topics T on Th.topic_id = T.id
        WHERE R.content ILIKE :pattern
        ORDER BY R.created_time ASC;
    """)

    pattern = f"%{query}%"
    result = db.session.execute(sql, {"pattern": pattern})

    replies = result.fetchall()

    formatted_replies = format_replies(replies)

    return formatted_replies

def format_replies(replies):
    formatted_replies = []

    for reply in replies:
        formatted_reply = {
            'id': reply.id,
            'username': reply.username,
            'content': reply.content.split("\n"),
            'created_time': reply.created_time.strftime("%d.%m.%Y at %H:%M:%S"),
            'thread_title': getattr(reply, 'thread_title', None),
            'thread_id': getattr(reply, 'thread_id', None),
            'topic_title': getattr(reply, 'topic_title', None),
            'topic_text_id': getattr(reply, 'topic_text_id', None)
        }
        formatted_replies.append(formatted_reply)

    return formatted_replies

def create_reply(thread_id, user_id, content):
    """Create a new reply."""
    sql = text("""
            INSERT INTO Replies (thread_id, user_id, content)
            VALUES (:thread_id, :user_id, :content)
            RETURNING id
                """)

    reply_id = db.session.execute(sql, {"thread_id": thread_id,
                                        "user_id": user_id,
                                        "content": content})

    db.session.commit()

    # Return first row of first column
    return reply_id.scalar()
