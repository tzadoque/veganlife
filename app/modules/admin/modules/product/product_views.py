import mimetypes
import os

from app import db
from app.config import Config
from app.forms import RegisterProduct, SearchProduct
from app.models.Product import Product
from flask import redirect, render_template, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename

from . import product


@product.route('/admin/products/', methods=('GET', 'POST'))
def product_list_view():

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  form = SearchProduct()

  if form.validate_on_submit():
    
    if form.search.data:
      return redirect(url_for('.result_product_search', search=form.search.data))

  products = Product.query.all()

  return render_template('product_list.html', products=products, form=form)

@product.route('/admin/products/s=<string:search>', methods=('GET', 'POST'))
def result_product_search(search):

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  form = SearchProduct()

  form.search.data = search

  products = Product.query.filter(Product.name.contains(form.search.data))
  
  return render_template('product_list.html', products=products, form=form)
  

@product.route('/admin/products/create', methods=('GET', 'POST'))
def product_create_view():

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  form = RegisterProduct()

  if form.validate_on_submit():

    product = Product()

    product.name = form.name.data
    product.category = form.category.data
    product.type = form.type.data
    product.description = form.description.data

    db.session.add(product)
    db.session.commit()

    if form.picture.data:

      file = form.picture.data
      file.filename = 'IMG_PRODUCT_' + str(product.id) + mimetypes.guess_extension(file.content_type)
      filename = secure_filename(file.filename)
      file.save(os.path.join( Config.UPLOAD_FOLDER + '/products', filename))

      product.picture = file.filename
    else:
      product.picture = "default.png"
      
    db.session.commit()

    return redirect(url_for('.product_list_view'))

  return render_template('create_product.html', products=Product(), form=form)

@product.route('/admin/products/edit/<int:id>', methods=('GET', 'POST'))
def product_edit_view(id):

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  form = RegisterProduct()

  product = Product.query.filter_by(id=id).first()

  form.name.data = product.name
  form.category.data = product.category
  form.type.data = product.type
  form.description.data = product.description

  return render_template('edit_product.html', form=form, product=product)

@product.route('/admin/products/edit/<int:id>/submit', methods=('GET', 'POST'))
def submit_product_edit(id):

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  form = RegisterProduct()

  product = Product.query.filter_by(id=id).first()

  if form.validate_on_submit():

    product.name = form.name.data
    product.category = form.category.data
    product.type = form.type.data
    product.description = form.description.data

    if form.picture.data:

      file = form.picture.data
      file.filename = 'IMG_PRODUCT_' + str(product.id) + mimetypes.guess_extension(file.content_type)
      filename = secure_filename(file.filename)
      file.save(os.path.join( Config.UPLOAD_FOLDER + '/products', filename))

      product.picture = file.filename
      db.session.commit()
    else:
      product.picture = product.picture
      db.session.commit()
    

    return redirect(url_for('admin.product.product_list_view'))

@product.route('/delete/<int:id>', methods=('GET', 'POST'))
def delete_product(id):

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  product = Product.query.filter_by(id=id).first()

  if product.picture != "default.png":
    file = os.path.join(Config.UPLOAD_FOLDER + '/products', product.picture)
    os.remove(file)

  db.session.delete(product)
  db.session.commit()
  return redirect(url_for('.product_list_view'))
