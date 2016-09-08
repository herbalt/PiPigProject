from flask import Blueprint
from pipig.sessions.models import Session

sessions = Blueprint('sessions', __name__)