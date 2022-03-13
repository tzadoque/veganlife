from app.models.Product import Product
from flask import redirect, render_template, url_for
from flask_login import current_user

from . import product


@product.route("/produtos/")
def products_list_view():

  if not current_user.is_active:
    return redirect(url_for('auth.login'))
  
  products = Product.query.all()
  
  return render_template("produtos.html", products=products)

@product.route("/produtos/<int:id>/")
def product_view(id):

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  product = Product.query.filter_by(id=id).first()

  return render_template("produto.html", product=product)
