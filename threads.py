from flask import request, session
from db import db
from sqlalchemy import text

def get_threads(topic):
    sql = text("""SELECT * FROM threads;""")
    result = db.session.execute(sql)

    return result.fetchall()