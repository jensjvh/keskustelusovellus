"""Module for handling routes of the app."""

from app import app
from flask import render_template, request, redirect, session


import users
import topics
import threads


@app.route("/")
def index():
    """Function for handling the root route."""
    return render_template("index.html", topics=topics.get_topics())


@app.route("/topics")
def view_topics():
    """Function for handling topics route."""
    return index()


@app.route("/topics/<topic>")
def view_threads(topic):
    """
    Function for handling a route for a particular topic

    Parameters
    ----------
    topic (str): String id of the topic.
    """
    topic_name = topic
    return render_template("threads.html", title=topic_name, threads=threads.get_threads(topic))


@app.route("/topics/<topic>/new_thread", methods=["get", "post"])
def new_thread(topic):
    """
    Function for handling a route for creating a thread for a particular topic.

    Parameters
    ----------
    topic (str): String id of the topic.
    """
    if request.method == "POST":
        title = request.form["title"]
        starting_reply = request.form["starting_reply"]

        threads.create_thread(title)

        return redirect(f"/topics/{topic}")
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
        return render_template("login.html", message="Incorrect username or password.")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404
