from flask_admin.contrib.sqla import ModelView
from wtforms.fields import PasswordField
from werkzeug.security import generate_password_hash
from flask_login import current_user

from app.models import User, Product
from app import db

class UserView(ModelView):

  form_edit_rules = ('name', 'last_name', 'birth_date', 'email')
  edit_modal = True

  form_extra_fields = {
    "password": PasswordField("Password")
  }

  column_filters = ['name', 'last_name', 'email', 'birth_date']

  column_exclude_list = ("password")

  def on_model_change(self, form, model, is_created):
    if is_created:
      model.password = generate_password_hash(form.password.data)

  def is_accessible(self):
    return current_user.is_authenticated

class ProductView(ModelView):
  column_filters = ['name', 'category', 'type']

def init_app(admin):
  admin.add_view(UserView(User, db.session))
  admin.add_view(ProductView(Product, db.session))