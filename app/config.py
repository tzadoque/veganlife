import os
class Config:
  SECRET_KEY = "SECRET"
  SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/uploads')