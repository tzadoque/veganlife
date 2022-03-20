from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def current_user(user_id):
  return User.query.get(user_id)

class User(db.Model, UserMixin):
  __tablename__ = "users"
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(84), nullable=False)
  last_name = db.Column(db.String(84))
  email = db.Column(db.String(84), nullable=False, unique=True, index=True)
  password = db.Column(db.String(12), nullable=False)
  profile_picture = db.Column(db.String(84))

  def __str__(self):
    return self.name