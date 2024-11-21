import os
from flask import request, session
from db import db
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import text

def login(username, password):
    sql = text("""SELECT password_hash, id, username, is_admin FROM users WHERE username=:username;""")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["admin"] = user.is_admin
            set_last_login(user.id)
            return True
        else:
            return False
        
def set_last_login(id):
    sql = text("""UPDATE users SET last_login=CURRENT_TIMESTAMP WHERE id=:id;""")
    db.session.execute(sql, {"id":id})
    db.session.commit()

def register(username, email, password):
    password_hash = generate_password_hash(password)
    try:
        sql = text("""INSERT INTO users (username, email, password_hash) VALUES (:username, :email, :password_hash);""")
        db.session.execute(sql, {"username":username, "email":email, "password_hash":password_hash})
        db.session.commit()
    except:
        return False
    return login(username, password)