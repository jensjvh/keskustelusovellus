from app import app
from flask import render_template, request, redirect, session

import users
import topics
import threads


@app.route("/")
def index():
    return render_template("index.html", topics=topics.get_topics())


@app.route("/topics")
def view_topics():
    return index()


@app.route("/topics/<topic>")
def view_threads(topic):
    topic_name = str(topic)
    return render_template("threads.html", title=topic_name, threads=threads.get_threads(topic))


@app.route("/topics/<topic>/new_thread")
def new_topic(topic):
    return render_template("new_thread.html")

@app.route("/register", methods=["get", "post"])
def register():
    # Check if user is already logged in
    if 'username' in session:
        return index()
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
    # Check if user is already logged in
    if 'username' in session:
        return index()
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
