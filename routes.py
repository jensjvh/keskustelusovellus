from app import app
from flask import render_template, request, redirect

import users

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if users.register(username, email, password):
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