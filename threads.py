"""A module for handling functionalities related to threads."""

from sqlalchemy import text
from db import db

import replies


def get_threads(topic):
    """Get threads from a given topic."""
    sql = text("""SELECT * FROM threads;""")
    result = db.session.execute(sql)

    return result.fetchall()

def create_thread(topic_id, user_id, title):
    sql = text("""
            INSERT INTO Threads (topic_id, user_id, title)
            VALUES (:topic_id, :user_id, :title)
                """)
    db.session.execute(sql, {"topic_id": topic_id,
                             "user_id": user_id,
                             "title": title})