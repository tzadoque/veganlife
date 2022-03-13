from flask import Blueprint

product = Blueprint("product", __name__, template_folder='templates')

from . import product_views