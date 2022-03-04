from flask import url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_login import current_user
from werkzeug.security import generate_password_hash
# from wtforms.fields import DateField, EmailField, FileField, PasswordField, SelectField, StringField, TextAreaField
# from wtforms.validators import DataRequired, regexp

from app import db
from app.models.Product import Product
from app.models.User import User

class UserView(BaseView):
  @expose('/', methods=('GET', 'POST'))
  def create_view(self):
    users = User.query.all()
    return self.render('admin/model/user.html', users=users)

class ProductView(BaseView):
  @expose('/', methods=('GET', 'POST'))
  def create_view(self):
    products = Product.query.all()
    return self.render('admin/model/product.html', products=products)


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

