import mimetypes
import os

from app import db
from app.config import Config
from app.forms import LoginUser, RegisterUser
from app.models.User import User
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from . import auth


@auth.route("/register/", methods=("GET", "POST"))
def register():
  form = RegisterUser()

  if form.validate_on_submit():

    user = User()

    if form.password.data != form.repeat_password.data:
      flash("As senhas precisam ser iguais", category="danger")
      return redirect(url_for('auth.register'))

    if User.query.filter_by(email=form.email.data).first():
      flash("O email já está registrado", category="danger")
      return redirect(url_for('auth.register'))
    
    user.name = form.name.data
    user.last_name = form.last_name.data
    user.birth_date = form.birth_date.data
    user.email = form.email.data
    user.password = generate_password_hash(form.password.data)

    db.session.add(user)
    db.session.commit()

    if form.profile_picture.data:
      file = form.profile_picture.data
      file.filename = 'IMG_PROFILE_' + str(user.id) + mimetypes.guess_extension(file.content_type)
      filename = secure_filename(file.filename)
      file.save(os.path.join( Config.UPLOAD_FOLDER + '/profiles', filename))

      user.profile_picture = file.filename
    else:
      user.profile_picture = "default.png"
    
    db.session.commit()

    login_user(user)
    return redirect(url_for("index"))

  return render_template("register.html", form=form)

@auth.route("/login/", methods=("GET", "POST"))
def login():
  form = LoginUser()

  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()

    if not user:
      flash("Email incorreto", category="danger")
      return redirect(url_for('auth.login'))

    if not check_password_hash(user.password, form.password.data):
      flash("Email correto", category="success")
      flash("Senha incorreta", category="danger")
      return redirect(url_for('auth.login'))

    login_user(user)
    return redirect(url_for("index"))

  return render_template("login.html", form=form)

@auth.route("/logout")
def logout():
  if not current_user.is_active:
    return redirect(url_for('.login'))

  logout_user()
  return redirect(url_for("index"))
