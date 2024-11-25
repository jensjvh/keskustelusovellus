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
            with open(schema_file, 'r') as file:
                schema_sql = file.read()

            db.session.execute(text(schema_sql))
            db.session.commit()
            print("Database schema created successfully.")
        except Exception as e:
            print(f"An error occurred while creating the schema: {e}")
            db.session.rollback()


def create_default_user():
    with app.app_context():
        try:
            sql = text(
                """INSERT INTO users (username, password_hash) VALUES (:username, :password_hash);"""
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
    with app.app_context():
        try:
            sql = text(
                """INSERT INTO users (username, password_hash, is_admin) VALUES (:username, :password_hash, TRUE);"""
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
    pass


def initialize_db():
    clear_all()
    create_default_user()
    create_admin_user()


if __name__ == "__main__":
    initialize_db()
