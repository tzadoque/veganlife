import mimetypes
import os

from flask import redirect, url_for, request
from flask_admin import BaseView, expose
from werkzeug.utils import secure_filename

from app import db
from app.config import Config
from app.forms import RegisterProduct, RegisterUser
from app.models.Product import Product
from app.models.User import User


class UserView(BaseView):
  @expose('/', methods=('GET', 'POST'))
  def create_view(self):

    form = RegisterUser()

    if form.validate_on_submit():
      
      user = User()

      user.name = form.name.data
      user.last_name = form.last_name.data
      user.birth_date = form.birth_date.data
      user.email = form.email.data
      user.password = form.password.data

      db.session.add(user)
      db.session.commit()

      if form.profile_picture:
        file = form.profile_picture.data
        file.filename = 'IMG_PROFILE_' + str(user.id) + mimetypes.guess_extension(file.content_type)
        filename = secure_filename(file.filename)
        file.save(os.path.join( Config.UPLOAD_FOLDER + '/profiles', filename))

        user.profile_picture = file.filename
        
        db.session.add(user)
        db.session.commit()

    return self.render('admin/model/user.html', users=User(), form=form)

  @expose('/delete/<int:id>', methods=('GET', 'POST'))
  def delete_view(self, id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('users.create_view'))

class ProductView(BaseView):
  @expose('/', methods=('GET', 'POST'))
  def create_view(self):

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

    return self.render('admin/model/product.html', products=Product(), form=form)
  
  @expose('/delete/<int:id>', methods=('GET', 'POST'))
  def delete_view(self, id):
    product = Product.query.filter_by(id=id).first()
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products.create_view'))


def init_app(admin):
  admin.add_view(UserView(name='Usuários', endpoint='users'))
  admin.add_view(ProductView(name='Produtos', endpoint='products'))

# class UserView(ModelView):

#   @expose('/usuario/', methods=('GET', 'POST'))
#   def create_view(self):

#     return self.render('create_user.html')

#   form_edit_rules = ('name', 'last_name', 'birth_date', 'email')
#   edit_modal = True

#   form_extra_fields = {
#     "name": StringField("Nome", validators={
#       DataRequired()
#     }),
#     "last_name": StringField("Sobrenome", validators={
#       DataRequired()
#     }),
#     "email": EmailField("E-mail", validators={
#       DataRequired()
#     }),
#     "password": PasswordField("Password", validators={
#       DataRequired()
#     }),
#     "birth_date": DateField("Data de nascimento")
#   }

#   column_filters = ['name', 'last_name', 'email', 'birth_date']

#   column_exclude_list = ("password")

#   def on_model_change(self, form, model, is_created):
#     if is_created:
#       model.password = generate_password_hash(form.password.data)

#   def is_accessible(self):
#     return current_user.is_authenticated

# class ProductView(ModelView):
#   edit_modal = True

#   product_categories = [
#     ('P', 'Proteínas'), 
#     ('HL', 'Higiene e Limpeza')
#   ]

#   form_extra_fields = {
#     "name": StringField("Nome", validators={DataRequired()}),
#     "description": TextAreaField("Descrição", validators={DataRequired()}),
#     "type": SelectField('Selecione o Tipo', choices=[('V', 'Vegano'), ('N', 'Não vegano')], validators={DataRequired()}),
#     "category": SelectField('Selecione a Categoria', choices=product_categories, validators={DataRequired()}),
#     "picture_upload": FileField('Imagem do produto'),
#     "picture": StringField('Caminho da imagem')
#   }

#   column_filters = [
#     "name",
#     FilterEqual(column=Product.category, name='Categorias', options=product_categories),
#     FilterEqual(column=Product.type, name="Tipos", options=[('V', 'Vegano'), ('N', 'Não vegano')])
#   ]

