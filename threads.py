"""A module for handling functionalities related to threads."""

from sqlalchemy import text
from db import db


MIN_TITLE_LENGTH = 1
MAX_TITLE_LENGTH = 50


def validate_title(title):
    """Validate thread title length."""
    if len(title) > MAX_TITLE_LENGTH or len(title) < MIN_TITLE_LENGTH:
        return False
    return True


def create_thread(topic_id, user_id, title):
    """
    A function for creating a thread with the given
    topic id, user id, and title.
    """
    sql = text("""
            INSERT INTO Threads (topic_id, user_id, title)
            VALUES (:topic_id, :user_id, :title)
            RETURNING id
                """)
    thread_id = db.session.execute(sql, {"topic_id": topic_id,
                                         "user_id": user_id,
                                         "title": title})

    db.session.commit()

    # Return first row of first column
    return thread_id.scalar()


def change_thread_title(thread_id, title):
    """
    A function for changing the title of an existing thread.
    """
    sql = text("""
               UPDATE threads
               SET title = :title
               WHERE id = :thread_id;
               """)

    db.session.execute(sql, {"title": title,
                             "thread_id": thread_id})

    db.session.commit()


def remove_threads_with_topic_id(topic_id):
    """Delete all threads and their replies with the given topic id."""
    thread_ids_sql = text("""
        SELECT id FROM threads
        WHERE topic_id = :topic_id;
    """)
    thread_ids_result = db.session.execute(thread_ids_sql, {"topic_id": topic_id})
    thread_ids = [row.id for row in thread_ids_result.fetchall()]

    for thread_id in thread_ids:
        delete_replies_sql = text("""
            DELETE FROM replies
            WHERE thread_id = :thread_id;
        """)
        db.session.execute(delete_replies_sql, {"thread_id": thread_id})

    delete_threads_sql = text("""
        DELETE FROM threads
        WHERE topic_id = :topic_id;
    """)
    db.session.execute(delete_threads_sql, {"topic_id": topic_id})

    db.session.commit()


def remove_thread(thread_id):
    """
    A function for removing a thread.
    """
    sql = text("""
               DELETE FROM threads
               WHERE id = :thread_id;
               """)

    db.session.execute(sql, {"thread_id": thread_id})

    db.session.commit()


def get_threads(topic):
    """Get threads from a given topic."""
    sql = text("""
        SELECT Th.id as id,
               Th.topic_id as topic_id,
               Th.user_id as user_id,
               Th.title as title,
               Th.created_time as created_time,
               Th.updated_time as updated_time,
               COUNT(R.id) as replies,
               MAX(R.created_time) AS last_reply
        FROM Threads Th
        LEFT JOIN Replies R ON Th.id = R.thread_id
        WHERE Th.topic_id = :topic_id
        GROUP BY Th.id
        ORDER BY last_reply DESC;
    """)
    result = db.session.execute(sql, {"topic_id": topic})

    threads = result.fetchall()

    formatted_threads = []

    for thread in threads:
        new_thread = {'id': thread.id,
                      'title': thread.title,
                      'topic_id': thread.topic_id,
                      'user_id': thread.user_id,
                      'created_time': thread.created_time,
                      'updated_time': thread.updated_time,
                      'replies': thread.replies,
                      }
        if thread.last_reply:
            new_thread['last_reply'] = thread.last_reply.strftime(
                "%Y.%m.%d at %H:%M:%S")
        else:
            new_thread['last_reply'] = 'No replies'

        formatted_threads.append(new_thread)

    return formatted_threads


def get_threads_by_user(user_id):
    """Get all threads with given user id."""
    sql = text("""
        SELECT Th.id, Th.title, Th.created_time, Th.updated_time, T.text_id as topic_text_id
        FROM threads Th
        INNER JOIN topics T ON Th.topic_id = T.id
        WHERE Th.user_id = :user_id
        ORDER BY Th.created_time DESC
    """)
    result = db.session.execute(sql, {"user_id": user_id})
    return result.fetchall()


def get_thread(thread_id):
    """Get thread with given id."""
    sql = text("""
        SELECT Th.id as id,
               Th.topic_id as topic_id,
               Th.user_id as user_id,
               U.username as username,
               Th.title as title,
               Th.created_time as created_time,
               Th.updated_time as updated_time,
               COUNT(R.id) as replies,
               MAX(R.created_time) AS last_reply
        FROM Threads Th
        LEFT JOIN Replies R ON Th.id = R.thread_id
        LEFT JOIN Users U ON Th.user_id = U.id
        WHERE Th.id = :id
        GROUP BY Th.id, U.username;
    """)
    result = db.session.execute(sql, {"id": thread_id})

    return result.fetchone()
