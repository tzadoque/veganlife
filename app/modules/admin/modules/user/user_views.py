import mimetypes
import os

from app import db
from app.config import Config
from app.forms import RegisterUser
from app.models.User import User
from flask import flash, redirect, render_template, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from . import user


@user.route('/admin/users/', methods=('GET', 'POST'))
def user_list_view():
  if not current_user.is_active:
    return redirect(url_for('auth.login'))
  return render_template('user_list.html', users=User())

@user.route('/admin/users/create', methods=('GET', 'POST'))
def user_create_view():
  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  form = RegisterUser()

  if form.validate_on_submit():

    user = User()

    if form.password.data != form.repeat_password.data:
      flash("As senhas precisam ser iguais", category="danger")
      return redirect(url_for(".user_create_view"))
    
    if User.query.filter_by(email=form.email.data).first():
      flash("O email já está registrado", category="danger")
      return redirect(url_for(".user_create_view"))

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
      user.profile_picture = "default.svg"

    db.session.commit()

    return redirect(url_for('.user_list_view'))

  return render_template('create_user.html', form=form)


@user.route('/admin/users/delete/<int:id>', methods=('GET', 'POST'))
def delete_user(id):
  if not current_user.is_active:
    return redirect(url_for('auth.login'))
  user = User.query.filter_by(id=id).first()

  if user.profile_picture and user.profile_picture != "default.svg":
    file = os.path.join(Config.UPLOAD_FOLDER + '/profiles', user.profile_picture)
    os.remove(file)

  db.session.delete(user)
  db.session.commit()
  return redirect(url_for('.user_list_view'))
