from flask_wtf import FlaskForm
from wtforms.fields import StringField, EmailField, PasswordField, BooleanField, SubmitField, DateField

class LoginForm(FlaskForm):
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  remember = BooleanField("Mantenha-me conectado.")
  submit = SubmitField("Entrar")

class RegisterForm(FlaskForm):
  name = StringField("Nome")
  last_name = StringField("Sobrenome")
  birth_date = DateField("Data de Nascimento")
  email = EmailField("E-mail")
  password = PasswordField("Senha")
  repeat_password = PasswordField("Repetir Senha")
  submit = SubmitField("Cadastrar")