from flask import Blueprint

notes_bp = Blueprint("notes", __name__)

from api.notes import views
