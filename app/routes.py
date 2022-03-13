from flask import redirect, render_template, url_for
from flask_login import current_user

from app.models.Product import Product

from app.modules.auth import auth as auth_blueprint
from app.modules.profile import profile as profile_blueprint
from app.modules.product import product as product_blueprint
from app.modules.admin import admin as admin_blueprint

def init_app(app):

  app.register_blueprint(auth_blueprint)
  app.register_blueprint(profile_blueprint)
  app.register_blueprint(product_blueprint)
  app.register_blueprint(admin_blueprint)

  @app.route("/")
  def index():
    if current_user.is_active:
      return render_template("home.html")
    return render_template("landing-page.html")

  # @app.route("/user/delete/<int:id>")
  # def delete(id):
  #   user = User.query.filter_by(id=id).first()
  #   db.session.delete(user)
  #   db.session.commit()

  #   return redirect("/")

  

  @app.errorhandler(404)
  def page_not_found(e):
    return render_template('404.html'), 404