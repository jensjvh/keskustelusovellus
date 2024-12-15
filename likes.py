"""A module for handling functionalities related to likes."""

from sqlalchemy import text
from db import db


def like_reply(user_id, reply_id):
    """Like a reply."""
    sql = text("""
        INSERT INTO likes (user_id, reply_id)
        VALUES (:user_id, :reply_id)
        ON CONFLICT DO NOTHING;
        """)
    
    db.session.execute(sql, {"user_id": user_id,
                             "reply_id": reply_id})
    db.session.commit()


def unlike_reply(user_id, reply_id):
    """Unlike a reply."""
    sql = text("""
            DELETE FROM likes
            WHERE user_id = :user_id AND reply_id = :reply_id;
        """)
    
    db.session.execute(sql, {"user_id": user_id,
                             "reply_id": reply_id})
    db.session.commit()


def has_liked_reply(user_id, reply_id):
    """Check if the user has liked the reply."""
    sql = text("""
        SELECT COUNT(*) FROM likes
        WHERE user_id = :user_id AND reply_id = :reply_id;
    """)
    result = db.session.execute(sql, {"user_id": user_id, "reply_id": reply_id})
    return result.scalar() > 0


def get_likes_by_user(user_id):
    """Get all likes by user id."""
    sql = text("""
        SELECT R.id as id, R.content as content, R.created_time as created_time,
               Th.title as thread_title, Th.id as thread_id,
               T.title as topic_title, T.text_id as topic_text_id,
               T.is_hidden as topic_is_hidden, U.username as reply_username
        FROM likes L
        INNER JOIN replies R ON L.reply_id = R.id
        INNER JOIN threads Th ON R.thread_id = Th.id
        INNER JOIN topics T ON Th.topic_id = T.id
        INNER JOIN users U on U.id = L.user_id
        WHERE L.user_id = :user_id
        ORDER BY L.created_time DESC
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()