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
import likes


def login_required(f):
    """Decorator for routes requiring a login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash("Please log in first", "message")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_only(f):
    """Decorator for routes requiring admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin', False):
            abort(403, description="Access restricted")
        return f(*args, **kwargs)
    return decorated_function


def admin_only_if_hidden(f):
    """Decorator for routes requiring admin if the topic is hidden."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        topic_text_id = kwargs.get('topic_text_id')
        topic = topics.get_topic_by_text_id(topic_text_id)
        if topic is None:
            abort(404, description="Topic not found")
        if topic.is_hidden and not session.get('is_admin', False):
            abort(403, description="Access restricted")
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


def check_topic_exists(f):
    """Decorator for checking if topic exists."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        topic_text_id = kwargs.get('topic_text_id')
        topic = topics.get_topic_by_text_id(topic_text_id)
        if topic is None:
            abort(404, description="Topic not found")
        return f(*args, **kwargs)
    return decorated_function


def check_thread_exists(f):
    """Decorator for checking if thread exists."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        thread_id = kwargs.get('thread_id')
        thread = threads.get_thread(thread_id)
        if thread is None:
            abort(404, description="Thread not found")
        return f(*args, **kwargs)
    return decorated_function


def check_reply_exists(f):
    """Decorator for checking if reply exists."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        reply_id = kwargs.get('reply_id')
        reply = replies.get_reply_by_id(reply_id)
        if reply is None:
            abort(404, description="Reply not found")
        return f(*args, **kwargs)
    return decorated_function

def generate_csrf_token():
    """Generate a csrf token."""
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']


@app.route("/")
def index():
    """Function for handling the root route."""
    generate_csrf_token()
    if session.get('is_admin'):
        topics_data = topics.get_all_topics()
    else:
        topics_data = topics.get_visible_topics()
    return render_template("index.html", topics=topics_data)


@app.route("/topics")
def view_topics():
    """Function for handling topics route."""
    return index()


@app.route("/topics/<topic_text_id>")
@check_topic_exists
@admin_only_if_hidden
def view_threads(topic_text_id):
    """
    Function for handling a route for a particular topic.

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    """
    topic = topics.get_topic_by_text_id(topic_text_id)

    threads_data = threads.get_threads(topic.id)

    return render_template("threads.html", topic=topic, threads=threads_data)


@app.route("/new_topic", methods=["get", "post"])
@admin_only
@login_required
@csrf_protected
def new_topic():
    """A function for handling new topic route."""
    if request.method == "POST":
        topic_text_id = request.form["topic_text_id"]
        topic_title = request.form["topic_title"]
        description = request.form["topic_description"]
        # Get is_hidden from the form checkbox
        is_hidden = request.form.get("is_hidden") == "on"

        if topics.validate_topic(topic_title, topic_text_id, description) is False:
            return redirect(url_for('new_topic'))

        if not topics.create_topic(topic_text_id, topic_title, description, is_hidden):
            flash("Topic already exists!", "error")
            return redirect(url_for('new_topic'))
        flash("Topic created successfully!", "message")
        return redirect(url_for('index'))

    return render_template("new_topic.html")


@app.route("/topics/<topic_text_id>/edit_topic", methods=["get", "post"])
@check_topic_exists
@admin_only
@login_required
@csrf_protected
def edit_topic(topic_text_id):
    """A function for handling edit topic route."""
    topic_record = topics.get_topic_by_text_id(topic_text_id)
    topic_id = topic_record.id

    if request.method == "POST":
        new_text_id = request.form["new_text_id"]
        new_title = request.form["new_title"]
        new_description = request.form["new_description"]
        is_hidden = request.form.get("is_hidden") == "on"
        if topics.validate_topic(new_title, new_text_id, new_description) is False:
            return redirect(url_for('edit_topic', topic_text_id=topic_text_id))
        if not topics.edit_topic_with_topic_id(topic_id, new_text_id, new_title, new_description, is_hidden):
            flash(f"A topic with the title {new_title} or text id {new_text_id} already exists")
            return redirect(url_for('edit_topic', topic_text_id=topic_text_id))
        flash(f'Changed topic title from {topic_record.title} to {new_title}')
        return redirect(url_for('index'))
    return render_template("edit_topic.html", topic_text_id=topic_record.text_id, topic=topic_record)


@app.route("/topics/<topic_text_id>/delete_topic", methods=["get", "post"])
@check_topic_exists
@admin_only
@login_required
@csrf_protected
def delete_topic(topic_text_id):
    """A function for handling delete topic route."""
    topic_record = topics.get_topic_by_text_id(topic_text_id)
    topic_id = topic_record.id

    if request.method == "POST":
        topics.remove_topic_with_topic_id(topic_id)
        flash(f'Topic {topic_record.title} with id {topic_id} removed')
        return redirect(url_for('index'))
    return render_template("delete_topic.html", topic=topic_record)


@app.route("/topics/<topic_text_id>/<thread_id>")
@check_thread_exists
@admin_only_if_hidden
def view_thread(topic_text_id, thread_id):
    """
    Function for handling a route for a particular thread

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    thread_id (int): id of the thread.
    """
    user_id = session.get("user_id")
    thread_data = threads.get_thread(thread_id)
    topic_data = topics.get_topic_by_text_id(topic_text_id)
    reply_data = replies.get_replies(thread_id, user_id)

    return render_template("view_thread.html",
                           thread=thread_data,
                           replies=reply_data,
                           topic=topic_data)


@app.route("/topics/<topic_text_id>/new_thread", methods=["get", "post"])
@check_topic_exists
@admin_only_if_hidden
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

        if threads.validate_title(title) is False:
            flash("Invalid title length", "error")
            return redirect(url_for('new_thread', topic_text_id=topic_text_id))

        if replies.validate_reply(starting_reply) is False:
            flash("Invalid starting reply length", "error")
            return redirect(url_for('new_thread', topic_text_id=topic_text_id))

        created_thread_id = threads.create_thread(topic_id, user_id, title)
        replies.create_reply(created_thread_id, user_id, starting_reply)
        flash("Thread created successfully!", "message")
        return redirect(url_for('view_threads', topic_text_id=topic_text_id))
    return render_template("new_thread.html", topic=topic_record)


@app.route("/topics/<topic_text_id>/<thread_id>/edit_thread", methods=["get", "post"])
@check_thread_exists
@admin_only_if_hidden
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

    if thread_record.user_id != session.get("user_id") and not session.get("is_admin", False):
        flash("You do not have permission to edit this thread", "error")
        return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id))

    if request.method == "POST":
        new_title = request.form["title"]

        if threads.validate_title(new_title) is False:
            flash("Invalid length for new title", "error")
            return redirect(url_for('edit_thread',
                                    topic_text_id=topic_text_id,
                                    thread_id=thread_id))

        threads.change_thread_title(thread_id, new_title)
        flash(
            f'Thread title changed from "{thread_record.title}" to "{new_title}"')
        return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id))
    return render_template("edit_thread.html", thread=thread_record, topic=topic_record)


@app.route("/topics/<topic_text_id>/<thread_id>/delete_thread", methods=["get", "post"])
@check_thread_exists
@admin_only
@login_required
@csrf_protected
def delete_thread(topic_text_id, thread_id):
    """
    Function for handling a route for deleting a thread.

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    thread_id (int): id of the thread.
    """
    topic_record = topics.get_topic_by_text_id(topic_text_id)
    thread_record = threads.get_thread(thread_id)
    thread_id = thread_record.id

    if request.method == "POST":
        threads.remove_thread(thread_id)
        flash(f'Thread {thread_record.title} with id {thread_id} removed')
        return redirect(url_for('view_threads', topic_text_id=topic_text_id))
    return render_template("delete_thread.html", thread=thread_record, topic=topic_record)


@app.route("/topics/<topic_text_id>/<thread_id>/new_reply", methods=["get", "post"])
@check_thread_exists
@admin_only_if_hidden
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
        if replies.validate_reply(content) is False:
            flash("Invalid reply length", "error")
            return render_template("new_reply.html", topic=topic_record, thread=thread_record)
        replies.create_reply(thread_id, user_id, content)
        flash("Reply sent")
        return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id))
    return render_template("new_reply.html", topic=topic_record, thread=thread_record)


@app.route("/topics/<topic_text_id>/<thread_id>/delete_reply/<int:reply_id>", methods=["get", "post"])
@check_thread_exists
@check_reply_exists
@login_required
@csrf_protected
def delete_reply(topic_text_id, thread_id, reply_id):
    """
    Function for handling a route for deleting a reply.

    Parameters
    ----------
    topic_text_id (str): String id of the topic.
    thread_id (int): id of the thread.
    reply_id (int): id of the reply.
    """
    reply = replies.get_reply_by_id(reply_id)
    if reply.user_id != session.get("user_id") and not session.get("is_admin", False):
        flash("You do not have permission to delete this reply", "error")
        return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id))

    replies.delete_reply(reply_id)
    flash("Reply deleted successfully", "message")
    return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id))


@app.route("/like_reply/<int:thread_id>/<int:reply_id>/<int:reply_index>", methods=["POST"])
@check_thread_exists
@check_reply_exists
@login_required
@csrf_protected
def like_reply(thread_id, reply_id, reply_index):
    """Handle liking a reply."""
    user_id = session.get("user_id")
    likes.like_reply(user_id, reply_id)

    thread = threads.get_thread(thread_id)
    topic = topics.get_topic_by_id(thread.topic_id)
    topic_text_id = topic.text_id

    return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id) + f"#{reply_index}")


@app.route("/unlike_reply/<int:thread_id>/<int:reply_id>/<int:reply_index>", methods=["POST"])
@check_thread_exists
@check_reply_exists
@login_required
@csrf_protected
def unlike_reply(thread_id, reply_id, reply_index):
    """Handle unliking a reply."""
    user_id = session.get("user_id")
    likes.unlike_reply(user_id, reply_id)

    thread = threads.get_thread(thread_id)
    topic = topics.get_topic_by_id(thread.topic_id)
    topic_text_id = topic.text_id

    return redirect(url_for('view_thread', topic_text_id=topic_text_id, thread_id=thread_id) + f"#{reply_index}")


@app.route("/profile")
@login_required
def profile():
    """Function for handling the profile route."""
    username = session.get("username")
    user_data = users.get_user_by_username(username)
    user_threads = threads.get_threads_by_user(user_data.id)
    user_replies = replies.get_replies_by_user(user_data.id)
    user_likes = likes.get_likes_by_user(user_data.id)
    return render_template("profile.html",
                           user=user_data,
                           threads=user_threads,
                           replies=user_replies,
                           likes=user_likes)


@app.route("/search", methods=["get", "post"])
@csrf_protected
def search():
    """Function for handling search route."""
    if request.method == "POST":
        query = request.form["query"]
        is_admin = session.get("is_admin", False)
        query_result = replies.get_matching_replies(query, is_admin)
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.validate_credentials(username, password) is False:
            flash("Invalid credentials", "error")
            return redirect(url_for("register"))

        if users.register(username, password):
            session["username"] = username
            session["csrf_token"] = generate_csrf_token()
            flash("Registration successful, welcome!", "message")
            return redirect(url_for("index"))
        flash("Username already exists", "error")
    return render_template("register.html")


@app.route("/login", methods=["get", "post"])
def login():
    """
    Function for handling login route.
    """
    # Check if user is already logged in
    if 'username' in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            session["csrf_token"] = generate_csrf_token()
            flash("Logged in successfully!", "message")
            return redirect(url_for("index"))
        flash("Incorrect username or password", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    """
    Function for handling logout route.
    """
    del session["user_id"]
    del session["username"]
    del session["is_admin"]
    del session["csrf_token"]
    flash("Logged out", "message")
    return redirect(url_for('index'))


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
    return render_template('error.html', error_message=e), 403
