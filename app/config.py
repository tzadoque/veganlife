import os

class Config:
  SECRET_KEY = "SECRET"
  SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False