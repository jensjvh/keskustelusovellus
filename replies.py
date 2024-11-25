"""A module for handling functionalities related to replies."""

from sqlalchemy import text
from db import db


def get_replies(thread):
    """Get replies from a specific thread."""
    sql = text("""SELECT * FROM replies;""")
    result = db.session.execute(sql)

    return result.fetchall()

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