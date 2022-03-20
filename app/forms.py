from flask_wtf import FlaskForm
from wtforms.fields import (BooleanField, EmailField, FileField, PasswordField,
                            SelectField, StringField, SubmitField,
                            TextAreaField)
from wtforms.validators import DataRequired

product_categories = [
  ("", "Selecione a Categoria"),
  ('P', 'Proteínas'), 
  ('HL', 'Higiene e Limpeza'),
  ('B', 'Bebidas'),
  ('GC', 'Grãos e cereais'),
  ('HF', 'HortiFruti'),
  ('L', 'Limpeza'),
  ('M', 'Mercearia')
]

class LoginUser(FlaskForm):
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  remember = BooleanField("Mantenha-me conectado.")
  submit = SubmitField("Entrar")

class RegisterUser(FlaskForm):
  name = StringField("Nome", validators={DataRequired()})
  last_name = StringField("Sobrenome")
  email = EmailField("E-mail", validators={DataRequired()})
  password = PasswordField("Senha")
  repeat_password = PasswordField("Repetir Senha")
  profile_picture = FileField("Imagem de perfil")
  submit = SubmitField("Cadastrar")

class RegisterProduct(FlaskForm):
  name = StringField("Nome do produto", validators={DataRequired()})
  category = SelectField('Selecione a Categoria', choices=product_categories, validators={DataRequired()})
  type = SelectField('Selecione o Tipo', choices=[("", "Selecione o Tipo"), ('V', 'Vegano'), ('N', 'Não vegano')], validators={DataRequired()})
  description = TextAreaField("Descrição", validators={DataRequired()})
  picture = FileField('Imagem do produto')
  submit = SubmitField('Cadastrar produto')


class SearchProduct(FlaskForm):
  search = StringField("Pesquise por nome, categoria ou tipo")
  category = SelectField('Selecione a Categoria', choices=product_categories)
  submit = SubmitField('Pesquisar')
