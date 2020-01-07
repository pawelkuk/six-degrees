"""In this package goes in the business logic of the app."""

from flask import Blueprint

bp = Blueprint("main", __name__)

from app.main import routes  # noqa
