from . import admin
from flask import render_template, url_for, redirect
from flask_login import current_user
from app.models.Product import Product
from app.models.User import User

from app.modules.admin.modules.user import user as user_blueprint
from app.modules.admin.modules.product import product as product_blueprint

admin.register_blueprint(user_blueprint)
admin.register_blueprint(product_blueprint)

@admin.route('/admin/')
def admin_home_view():
  if not current_user.is_active:
    return redirect(url_for('auth.login'))
  products = Product()
  users = User()
  return redirect(url_for('admin.product.product_list_view'))
  # return render_template('admin_home.html', products=products, users=users)