from flask import request, session
from db import db
from sqlalchemy import text


def get_topics():
    sql = text("""SELECT * FROM topics;""")
    result = db.session.execute(sql)

    return result.fetchall()
