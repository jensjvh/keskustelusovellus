"""Module for running the flask app."""

from os import getenv
from flask import Flask


app = Flask(__name__, static_folder='static')
app.secret_key = getenv("SECRET_KEY")

app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

import routes
