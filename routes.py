"""Module for handling routes of the app."""

from app import app
from datetime import datetime
from functools import wraps
from flask import render_template, request, redirect, session, url_for, abort, flash
import secrets


import users
import topics
import threads
import replies


def login_required(f):
    """Decorator for routes requiring a login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in first", "message")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def csrf_protected(f):
    """Decorator for protecting routes against CSRF attacks."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Apply only to POST requests
        if request.method == "POST":
            token_in_form = request.form.get("csrf_token")
            token_in_session = session.get("csrf_token")
            if not token_in_form or token_in_form != token_in_session:
                abort(403, description="Invalid CSRF token")
        return f(*args, **kwargs)
    return decorated_function


def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']


@app.route("/")
def index():
    """Function for handling the root route."""
    generate_csrf_token()
    return render_template("index.html", topics=topics.get_topics())


@app.route("/topics")
def view_topics():
    """Function for handling topics route."""
    return index()


@app.route("/topics/<topic_text_id>")
def view_threads(topic_text_id):
    """
    Function for handling a route for a particular topic

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    """
    topic = topics.get_topic_by_text_id(topic_text_id)
    threads_data = threads.get_threads(topic.id)

    return render_template("threads.html", topic=topic, threads=threads_data)


@app.route("/topics/<topic_text_id>/<thread_id>")
def view_thread(topic_text_id, thread_id):
    """
    Function for handling a route for a particular thread

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    thread_id (int): id of the thread.
    """
    thread_data = threads.get_thread(thread_id)
    reply_data = replies.get_replies(thread_id)

    return render_template("view_thread.html",
                           thread=thread_data,
                           replies=reply_data)


@app.route("/topics/<topic_text_id>/new_thread", methods=["get", "post"])
@login_required
@csrf_protected
def new_thread(topic_text_id):
    """
    Function for handling a route for creating a thread for a particular topic.

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    """
    topic_record = topics.get_topic_by_text_id(topic_text_id)
    topic_id = topic_record.id

    if request.method == "POST":
        user_id = session.get("user_id")
        title = request.form["title"]

        starting_reply = request.form["starting_reply"]

        created_thread_id = threads.create_thread(topic_id, user_id, title)
        replies.create_reply(created_thread_id, user_id, starting_reply)
        flash("Thread created successfully!", "message")
        return redirect(url_for('view_threads', topic_text_id=topic_text_id))
    return render_template("new_thread.html", topic=topic_record)


@app.route("/topics/<topic_text_id>/<thread_id>/edit_thread", methods=["get", "post"])
@login_required
@csrf_protected
def edit_thread(topic_text_id, thread_id):
    """
    Function for handling a route for editing a thread.

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    thread_id (int): id of the thread.
    """
    topic_record = topics.get_topic_by_text_id(topic_text_id)
    thread_record = threads.get_thread(thread_id)
    thread_id = thread_record.id

    if thread_record.user_id != session.get("user_id"):
        flash("You do not have permission to edit this thread", "error")
        return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id))

    if request.method == "POST":
        new_title = request.form["title"]
        threads.change_thread_title(thread_id, new_title)
        flash(f'Thread title changed from "{thread_record.title}" to "{new_title}"')
        return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id = thread_id))
    return render_template("edit_thread.html", thread = thread_record,topic=topic_record)


@app.route("/topics/<topic_text_id>/<thread_id>/new_reply", methods=["get", "post"])
@login_required
@csrf_protected
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
        flash("Reply sent")
        return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id))
    return render_template("new_reply.html", topic=topic_record, thread=thread_record)

@app.route("/profile")
@login_required
def profile():
    """Function for handling the profile route."""
    username = session.get("username")
    user_data = users.get_user_by_username(username)
    user_threads = threads.get_threads_by_user(user_data.id)
    user_replies = replies.get_replies_by_user(user_data.id)
    return render_template("profile.html", user=user_data, threads=user_threads, replies=user_replies)

@app.route("/search", methods=["get", "post"])
@csrf_protected
def search():
    """Function for handling search route."""
    if request.method == "POST":
        query = request.form["query"]
        query_result = replies.get_matching_replies(query)
        return render_template("search_results.html", query=query, query_result=query_result)
    return render_template("search.html")

@app.route("/register", methods=["get", "post"])
@csrf_protected
def register():
    """
    Function for handling register route.
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
            session["csrf_token"] = generate_csrf_token()
            flash("Registration successful, welcome!", "message")
            return redirect("/")
        flash("Invalid username or password", "error")
        return render_template("register.html")


@app.route("/login", methods=["get", "post"])
def login():
    """
    Function for handling login route.
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
            session["csrf_token"] = generate_csrf_token()
            flash("Logged in successfully!", "message")
            return redirect("/")
        flash("Incorrect username or password", "error")
        return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Function for handling logout route.
    """
    del session["username"]
    del session["csrf_token"]
    flash("Logged out", "message")
    return redirect("/")


@app.errorhandler(404)
def page_not_found(e):
    """
    Function for rendering error template when running into a 404 error.
    """
    return render_template('error.html', error_message="Page not found"), 404

@app.errorhandler(403)
def forbidden(e):
    """
    Function for rendering error template when running into a 403 error.
    """
    return render_template('error.html', error_message="Access forbidden"), 403
