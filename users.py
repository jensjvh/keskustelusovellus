"""Module for handling database functionalities related to users"""
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from db import db


MIN_USERNAME_LENGTH = 2
MAX_USERNAME_LENGTH = 15
MIN_PASSWORD_LENGTH = 8


def validate_credentials(username, password):
    """Validate length of username and password, and the format of username."""
    if not username.isalnum():
        return False
    if len(username) < MIN_USERNAME_LENGTH or len(username) > MAX_USERNAME_LENGTH:
        return False
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    return True


def login(username, password):
    """Handle user login."""
    sql = text(
        """SELECT password_hash, id, username, is_admin FROM users WHERE username=:username;""")
    result = db.session.execute(sql, {"username": username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        session["username"] = user.username
        session["is_admin"] = user.is_admin
        set_last_login(user.id)
        return True
    return False


def get_user_by_username(username):
    """Get user with the given username."""
    sql = text("""
        SELECT id, username, created_time
        FROM users
        WHERE username = :username
    """)
    result = db.session.execute(sql, {"username": username})
    return result.fetchone()


def set_last_login(user_id):
    """Set the last login time of the user."""
    sql = text("""UPDATE users SET last_login=CURRENT_TIMESTAMP WHERE id=:id;""")
    db.session.execute(sql, {"id": user_id})
    db.session.commit()


def register(username, password):
    """Handle user registration."""
    password_hash = generate_password_hash(password)
    try:
        sql = text(
            """INSERT INTO users (username, password_hash) VALUES (:username, :password_hash);""")
        db.session.execute(
            sql, {"username": username, "password_hash": password_hash})
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return False
    return login(username, password)
