from flask import render_template

from app.modules.auth import auth as auth_blueprint
from app.modules.profile import profile as profile_blueprint
from app.modules.product import product as product_blueprint
from app.modules.admin import admin as admin_blueprint
from app.modules.home import home as home_blueprint

def init_app(app):

  app.register_blueprint(auth_blueprint)
  app.register_blueprint(profile_blueprint)
  app.register_blueprint(product_blueprint)
  app.register_blueprint(admin_blueprint)
  app.register_blueprint(home_blueprint)

  @app.errorhandler(404)
  def page_not_found(e):
    return render_template('404.html'), 404