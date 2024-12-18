"""A module for handling functionalities related to replies."""

from sqlalchemy import text
from db import db


REPLY_MIN_LENGTH = 1
REPLY_MAX_LENGTH = 1000


def get_replies(thread_id, user_id):
    """Get replies from a specific thread."""
    sql = text("""
            SELECT R.id as id,
                   U.username as username,
                   U.id as user_id,
                   R.content as content,
                   R.created_time as created_time,
                   R.is_edited as is_edited,
                   (SELECT COUNT(*) FROM likes L
                   WHERE L.reply_id = R.id) as likes,
                   EXISTS (SELECT 1 FROM likes L
                   WHERE L.user_id = :user_id AND L.reply_id = R.id) as has_liked
            FROM replies R
            INNER JOIN threads Th ON Th.id = R.thread_id
            INNER JOIN users U on R.user_id = U.id
            WHERE R.thread_id = :thread_id
            ORDER BY R.created_time ASC;""")

    result = db.session.execute(sql, {"thread_id": thread_id,
                                      "user_id": user_id})

    replies = result.fetchall()

    formatted_replies = format_replies(replies)

    return formatted_replies


def get_reply_by_id(reply_id):
    """Function for getting a reply by id."""
    sql = text("""
            SELECT thread_id, user_id, content
            FROM replies WHERE id = :reply_id
            """)
    result = db.session.execute(sql, {"reply_id": reply_id})
    return result.fetchone()


def delete_reply(reply_id):
    """Function for deleting a reply by id."""
    sql = text("DELETE FROM replies WHERE id = :reply_id")
    db.session.execute(sql, {"reply_id": reply_id})
    db.session.commit()


def get_replies_by_user(user_id):
    """Function for getting all replies with user id."""
    sql = text("""
        SELECT R.id as id, R.content as content, R.created_time as created_time,
               Th.title as thread_title, Th.id as thread_id,
               T.title as topic_title, T.text_id as topic_text_id,
               T.is_hidden as topic_is_hidden
        FROM replies R
        INNER JOIN threads Th ON R.thread_id = Th.id
        INNER JOIN topics T ON Th.topic_id = T.id
        WHERE R.user_id = :user_id
        ORDER BY R.created_time DESC
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def get_matching_replies(query, is_admin):
    """Get replies matching a pattern."""
    if is_admin:
        sql = text("""
            SELECT R.id as id,
                   U.username as username,
                   U.id as user_id,
                   R.content as content,
                   R.created_time as created_time,
                   Th.title as thread_title,
                   Th.id as thread_id,
                   T.title as topic_title,
                   T.text_id as topic_text_id,
                   T.is_hidden as is_hidden
            FROM replies R
            INNER JOIN users U on R.user_id = U.id
            INNER JOIN threads Th on R.thread_id = Th.id
            INNER JOIN topics T on Th.topic_id = T.id
            WHERE R.content ILIKE :pattern
            ORDER BY R.created_time ASC;
        """)
        params = {"pattern": f"%{query}%"}
    else:
        sql = text("""
            SELECT R.id as id,
                   U.username as username,
                   U.id as user_id,
                   R.content as content,
                   R.created_time as created_time,
                   Th.title as thread_title,
                   Th.id as thread_id,
                   T.title as topic_title,
                   T.text_id as topic_text_id,
                   T.is_hidden as is_hidden
            FROM replies R
            INNER JOIN users U on R.user_id = U.id
            INNER JOIN threads Th on R.thread_id = Th.id
            INNER JOIN topics T on Th.topic_id = T.id
            WHERE R.content ILIKE :pattern
            AND T.is_hidden = FALSE
            ORDER BY R.created_time ASC;
        """)
        params = {"pattern": f"%{query}%"}

    result = db.session.execute(sql, params)

    replies = result.fetchall()

    formatted_replies = format_replies(replies)

    return formatted_replies


def format_replies(replies):
    """Format replies to securely add newlines to user reply."""
    formatted_replies = []

    for reply in replies:
        formatted_reply = {
            'id': reply.id,
            'username': reply.username,
            'user_id': reply.user_id,
            'content': reply.content.split("\n"),
            'created_time': reply.created_time,
            'thread_title': getattr(reply, 'thread_title', None),
            'thread_id': getattr(reply, 'thread_id', None),
            'topic_title': getattr(reply, 'topic_title', None),
            'topic_text_id': getattr(reply, 'topic_text_id', None),
            'likes': getattr(reply, 'likes', None),
            'has_liked': getattr(reply, 'has_liked', None),
            'is_hidden': getattr(reply, 'is_hidden', None),
            'is_edited': getattr(reply, 'is_edited', None)
        }
        formatted_replies.append(formatted_reply)

    return formatted_replies


def validate_reply(reply):
    """Validate reply length."""
    if len(reply) > REPLY_MAX_LENGTH or len(reply) < REPLY_MIN_LENGTH:
        return False
    return True


def remove_replies_with_thread_id(thread_id):
    """Delete all replies with given thread id."""
    sql = text("""
               DELETE FROM replies
               WHERE thread_id = :thread_id;
               """)

    db.session.execute(sql, {"thread_id": thread_id})

    db.session.commit()


def edit_reply(reply_id, content):
    """Edit a reply."""
    sql = text("""
            UPDATE replies
            SET content = :content,
                is_edited = TRUE
            WHERE id = :reply_id
                """)

    db.session.execute(sql, {"reply_id": reply_id,
                             "content": content})

    db.session.commit()


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
