from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from app.config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  login_manager.init_app(app)

  from app import routes
  routes.init_app(app)

  # register admin page
  from app.admin import AdminHomeView
  admin = Admin(
    app,
    index_view=AdminHomeView(
      name='Home',
      template='admin/myhome.html',
      url='/admin'
    )
  )
  from app import admin as administrator
  administrator.init_app(admin)

  return app

