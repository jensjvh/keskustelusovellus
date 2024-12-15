"""
A module for inserting default values into the tables of the app.
"""

from sqlalchemy import text
from werkzeug.security import generate_password_hash
from app import app
from db import db


def clear_all():
    """
    Execute a raw SQL schema to create tables and initialize the database.
    """
    with app.app_context():
        try:
            schema_file = 'schema.sql'
            with open(schema_file, 'r', encoding="utf-8") as file:
                schema_sql = file.read()

            db.session.execute(text(schema_sql))
            db.session.commit()
            print("Database schema created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the schema: {e}")
            db.session.rollback()


def create_default_user():
    """
    Create a default user.
    username: user
    password: defaultpassword
    """
    with app.app_context():
        try:
            sql = text(
                """INSERT INTO users (username, password_hash)
                   VALUES (:username, :password_hash);"""
            )
            password_hash = generate_password_hash("defaultpassword")
            db.session.execute(
                sql, {"username": "user",
                      "password_hash": password_hash}
            )
            db.session.commit()
            print("Default user created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the default user: {e}")


def create_admin_user():
    """
    Create a default admin user.
    username: admin
    password: adminpassword
    """
    with app.app_context():
        try:
            sql = text(
                """INSERT INTO users (username, password_hash, is_admin)
                   VALUES (:username, :password_hash, TRUE);"""
            )
            password_hash = generate_password_hash("adminpassword")
            db.session.execute(
                sql, {"username": "admin",
                      "password_hash": password_hash}
            )
            db.session.commit()
            print("Admin user created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the admin user: {e}")


def create_topics():
    """
    Create default topics:
    General Discussion,
    Announcements,
    Feedback,
    Hidden.
    """
    with app.app_context():
        try:
            sql = text(
                """INSERT INTO topics (text_id, title, description, is_hidden)
                   VALUES (:text_id, :title, :description, :is_hidden);"""
            )
            db.session.execute(
                sql, {"text_id": "general_discussion",
                      "title": "General Discussion",
                      "description": "Discuss anything.",
                      "is_hidden": False}
            )
            db.session.execute(
                sql, {"text_id": "announcements",
                      "title": "Announcements",
                      "description": "Forum announcements.",
                      "is_hidden": False}
            )
            db.session.execute(
                sql, {"text_id": "feedback",
                      "title": "Feedback",
                      "description": "Give us feedback.",
                      "is_hidden": False}
            )
            db.session.execute(
                sql, {"text_id": "hidden",
                      "title": "Hidden",
                      "description": "This should be invisible to normal users.",
                      "is_hidden": True}
            )
            db.session.commit()
            print("Default topics created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the default topics: {e}")


def create_threads_and_replies():
    """
    Create default threads and replies.
    """
    with app.app_context():
        try:
            thread_sql = text(
                """INSERT INTO threads (topic_id, user_id, title)
                   VALUES (:topic_id, :user_id, :title);"""
            )
            reply_sql = text(
                """INSERT INTO replies (thread_id, user_id, content)
                   VALUES (:thread_id, :user_id, :content);"""
            )
            db.session.execute(
                thread_sql, {"topic_id": 1,
                      "user_id": 1,
                      "title": "User's thread"}
            )
            db.session.execute(
                reply_sql, {"thread_id": 1,
                      "user_id": 1,
                      "content": "New\nline"}
            )
            db.session.execute(
                reply_sql, {"thread_id": 1,
                      "user_id": 1,
                      "content": "A starting reply"}
            )
            db.session.execute(
                thread_sql, {"topic_id": 1,
                      "user_id": 2,
                      "title": "Admin's thread"}
            )
            db.session.execute(
                reply_sql, {"thread_id": 2,
                      "user_id": 2,
                      "content": "Admin starting reply"}
            )
            db.session.execute(
                thread_sql, {"topic_id": 4,
                      "user_id": 2,
                      "title": "Hidden thread"}
            )
            db.session.execute(
                reply_sql, {"thread_id": 3,
                      "user_id": 2,
                      "content": "Hidden thread starting reply"}
            )
            db.session.commit()
            print("Default threads and replies created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the default threads and replies: {e}")
        

def initialize_db():
    """Execute all specified functions."""
    print("Initializing database...")
    clear_all()
    create_default_user()
    create_admin_user()
    create_topics()
    create_threads_and_replies()


if __name__ == "__main__":
    initialize_db()
