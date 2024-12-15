"""A module for creating the db connection for Flask."""

from os import getenv
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from app import app

load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("://", "ql://", 1)
db = SQLAlchemy(app)
