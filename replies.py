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

    formatted_replies = []

    for reply in replies:
        formatted_reply = {'id': reply.id,
                      'username': reply.username,
                      'content': reply.content,
                      'created_time': reply.created_time
                     }
        formatted_reply['created_time'] = reply.created_time.strftime("%d.%m.%Y at %H:%M:%S")

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
