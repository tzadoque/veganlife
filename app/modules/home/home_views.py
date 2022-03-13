from flask import render_template
from flask_login import current_user

from . import home


@home.route("/")
def index_view():
  
  if not current_user.is_active:
    return render_template("landing-page.html")

  return render_template("home.html")
