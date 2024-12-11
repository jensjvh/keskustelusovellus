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
    Feedback.
    """
    with app.app_context():
        try:
            sql = text(
                """INSERT INTO topics (text_id, title, description)
                   VALUES (:text_id, :title, :description);"""
            )
            db.session.execute(
                sql, {"text_id": "general_discussion",
                      "title": "General Discussion",
                      "description": "Discuss anything."}
            )
            db.session.execute(
                sql, {"text_id": "announcements",
                      "title": "Announcements",
                      "description": "Forum announcements."}
            )
            db.session.execute(
                sql, {"text_id": "feedback",
                      "title": "Feedback",
                      "description": "Give us feedback."}
            )
            db.session.commit()
            print("Default topics created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the default topics: {e}")


def initialize_db():
    """Execute all specified functions."""
    print("Initializing database...")
    clear_all()
    create_default_user()
    create_admin_user()
    create_topics()


if __name__ == "__main__":
    initialize_db()
