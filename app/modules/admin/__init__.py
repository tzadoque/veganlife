from flask import Blueprint

admin = Blueprint("admin", __name__, template_folder='templates')

from . import admin_views