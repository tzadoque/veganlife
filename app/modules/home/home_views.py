from flask import render_template, redirect, url_for
from flask_login import current_user

from . import home


@home.route("/")
def index_view():
  
  if not current_user.is_active:
    return render_template("landing-page.html")

  return redirect(url_for('product.products_list_view'))
