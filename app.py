"""Module for running the flask app."""

from os import getenv
from flask import Flask


app = Flask(__name__, static_folder='static')
app.secret_key = getenv("SECRET_KEY")

import routes
