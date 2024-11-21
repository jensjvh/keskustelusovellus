"""A module for handling functionalities related to threads."""

from flask import request, session
from sqlalchemy import text
from db import db



def get_threads(topic):
    """Get threads from a given topic."""
    sql = text("""SELECT * FROM threads;""")
    result = db.session.execute(sql)

    return result.fetchall()
