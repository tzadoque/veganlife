import mimetypes
import os

from flask import flash, redirect, url_for, request
from flask_admin import BaseView, AdminIndexView, expose
from flask_login import current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from app import db
from app.config import Config
from app.forms import RegisterProduct, RegisterUser
from app.models.Product import Product
from app.models.User import User


class UserView(BaseView):
  @expose('/', methods=('GET', 'POST'))
  def list_view(self):
    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"
    return self.render('admin/model/users.html', users=User())

  @expose('/create', methods=('GET', 'POST'))
  def create_view(self):
    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"

    form = RegisterUser()

    if form.validate_on_submit():

      user = User()

      if form.password.data != form.repeat_password.data:
        flash("As senhas precisam ser iguais", category="danger")
        return redirect(url_for("users.create_view"))
      
      if User.query.filter_by(email=form.email.data).first():
        flash("O email já está registrado", category="danger")
        return redirect(url_for("users.create_view"))

      user.name = form.name.data
      user.last_name = form.last_name.data
      user.birth_date = form.birth_date.data
      user.email = form.email.data
      user.password = generate_password_hash(form.password.data)

      if form.profile_picture.data:
        file = form.profile_picture.data
        file.filename = 'IMG_PROFILE_' + str(user.id) + mimetypes.guess_extension(file.content_type)
        filename = secure_filename(file.filename)
        file.save(os.path.join( Config.UPLOAD_FOLDER + '/profiles', filename))

        user.profile_picture = file.filename
        
        db.session.add(user)
        db.session.commit()
      else:
        db.session.add(user)
        db.session.commit()

      return redirect(url_for('users.list_view'))

    return self.render('admin/model/create_user.html', form=form)


  @expose('/delete/<int:id>', methods=('GET', 'POST'))
  def delete_view(self, id):
    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.list_view'))

class ProductView(BaseView):
  @expose('/', methods=('GET', 'POST'))
  def list_view(self):
    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"
    return self.render('admin/model/products.html', products=Product())

  @expose('/create', methods=('GET', 'POST'))
  def create_view(self):

    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"

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
        
        db.session.add(product)
        db.session.commit()

      return redirect(url_for('products.list_view'))

    return self.render('admin/model/create_product.html', products=Product(), form=form)

  @expose('/edit/<int:id>', methods=('GET', 'POST'))
  def edit_view(self, id):
    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"

    form = RegisterProduct()

    product = Product.query.filter_by(id=id).first()

    form.name.data = product.name
    form.category.data = product.category
    form.type.data = product.type
    form.description.data = product.description

    return self.render('admin/model/edit_product.html', form=form, product=product)

  @expose('/edit/<int:id>/submit', methods=('GET', 'POST'))
  def edit_submit(self, id):
    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"
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
      

      return redirect(url_for('products.list_view'))

  @expose('/delete/<int:id>', methods=('GET', 'POST'))
  def delete_view(self, id):
    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products.list_view'))

class AdminHomeView(AdminIndexView):
  @expose('/')
  def index(self):
    if not current_user.is_active:
      return "VOCÊ NÃO TEM AUTORIZAÇÃO PARA ACESSAR ESSA PÁGINA"
    products = Product()
    users = User()
    return self.render('admin/index.html', products=products, users=users)

def init_app(admin):
  admin.add_view(UserView(name='Usuários', endpoint='users'))
  admin.add_view(ProductView(name='Produtos', endpoint='products'))