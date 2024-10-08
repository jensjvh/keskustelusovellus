from app import app
from flask import render_template, request, redirect, session

import users
import threads

@app.route("/")
def index():
    return render_template("index.html", topics = threads.get_topics())

@app.route("/topics")
def topics():
    return index()

@app.route("/topics/<name>")
def topic(name):
    return index()

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if users.register(username, email, password):
            session["username"] = username
            return redirect("/")
        else:
            return render_template("register.html", message="Incorrect username or password.")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("login.html", message="Incorrect username or password.")
        
@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404