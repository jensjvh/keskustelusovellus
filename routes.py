"""Module for handling routes of the app."""

from app import app
from datetime import datetime
from functools import wraps
from flask import render_template, request, redirect, session, url_for


import users
import topics
import threads
import replies


def login_required(f):
    """Function used for decorating routes requiring a login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    """Function for handling the root route."""
    return render_template("index.html", topics=topics.get_topics())


@app.route("/topics")
def view_topics():
    """Function for handling topics route."""
    return index()


@app.route("/topics/<text_id>")
def view_threads(text_id):
    """
    Function for handling a route for a particular topic

    Parameters
    ----------
    text_id (str): String id of the topic.
    """
    topic = topics.get_topic_by_text_id(text_id)
    threads_data = threads.get_threads(topic.id)

    return render_template("threads.html", topic=topic, threads=threads_data)


@app.route("/topics/<topic_text_id>/<thread_id>")
def view_thread(topic_text_id, thread_id):
    """
    Function for handling a route for a particular thread

    Parameters
    ----------
    text_id (str): String id of the topic.
    thread_id (int): id of the thread.
    """
    thread_data = threads.get_thread(thread_id)
    reply_data = replies.get_replies(thread_id)

    return render_template("view_thread.html",
                           thread=thread_data,
                           replies=reply_data)


@app.route("/topics/<topic_text_id>/new_thread", methods=["get", "post"])
@login_required
def new_thread(topic_text_id):
    """
    Function for handling a route for creating a thread for a particular topic.

    Parameters
    ----------
    topic (str): String id of the topic.
    """
    topic_record = topics.get_topic_by_text_id(topic_text_id)
    topic_id = topic_record.id

    if request.method == "POST":
        user_id = session.get("user_id")
        title = request.form["title"]

        starting_reply = request.form["starting_reply"]

        created_thread_id = threads.create_thread(topic_id, user_id, title)
        replies.create_reply(created_thread_id, user_id, starting_reply)

        return redirect(url_for('view_threads', text_id=topic_text_id))
    return render_template("new_thread.html", topic=topic_record)


@app.route("/topics/<topic_text_id>/<thread_id>/new_reply", methods=["get", "post"])
@login_required
def new_reply(topic_text_id, thread_id):
    """
    Function for handling a route for creating a reply inside a thread.

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    thread_id (int): id of the thread.
    """
    topic_record = topics.get_topic_by_text_id(topic_text_id)
    thread_record = threads.get_thread(thread_id)
    thread_id = thread_record.id
    topic_id = topic_record.id

    if request.method == "POST":
        user_id = session.get("user_id")
        content = request.form["reply"]
        replies.create_reply(thread_id, user_id, content)

        return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id))
    return render_template("new_reply.html", topic=topic_record, thread=thread_record)


@app.route("/register", methods=["get", "post"])
def register():
    """
    Function for registering a user.
    """
    # Check if user is already logged in
    if 'username' in session:
        return index()
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            session["username"] = username
            return redirect("/")
        return render_template("register.html", message="Incorrect username or password.")


@app.route("/login", methods=["get", "post"])
def login():
    """
    Function for logging in a user.
    """
    # Check if user is already logged in
    if 'username' in session:
        return index()
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        return render_template("login.html", message="Incorrect username or password.")


@app.route("/logout")
def logout():
    """
    Function for logging out a user.
    """
    del session["username"]
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    """
    Function for rendering error template when running into an error.
    """
    return render_template('404.html'), 404
