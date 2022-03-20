import mimetypes
import os

from app import db
from app.config import Config
from app.forms import RegisterUser
from app.models.User import User
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, logout_user
from werkzeug.utils import secure_filename

from . import profile


@profile.route("/profile/")
def profile_view():

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  user = User.query.filter_by(id=current_user.id).first()

  return render_template("profile.html", user=user)
  
@profile.route("/profile/edit", methods=("GET", "POST"))
def edit_profile():

  if not current_user.is_active:
    return redirect(url_for('auth.login'))
  
  form = RegisterUser()

  user = User.query.filter_by(id=current_user.id).first()

  form.name.data = user.name
  form.last_name.data = user.last_name
  form.email.data = user.email

  return render_template("edit_profile.html", user=user, form=form)

@profile.route("/profile/edit/submit", methods=("GET", "POST"))
def submit_profile_edit():
  
  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  form = RegisterUser()

  user = User.query.filter_by(id=current_user.id).first()

  if form.validate_on_submit():

    if User.query.filter_by(email=form.email.data).first():
      if form.email.data != user.email:
        flash("O email já está registrado", category="danger")
        return redirect(url_for("edit_profile"))

    user.name = form.name.data
    user.last_name = form.last_name.data
    user.email = form.email.data

    if form.profile_picture.data:

      file = form.profile_picture.data
      file.filename = 'IMG_PROFILE_' + str(user.id) + mimetypes.guess_extension(file.content_type)
      filename = secure_filename(file.filename)
      file.save(os.path.join( Config.UPLOAD_FOLDER + '/profiles', filename))

      user.profile_picture = file.filename
    else:
      user.profile_picture = user.profile_picture

    db.session.commit()

    return redirect(url_for('profile.profile_view'))

@profile.route('/profile/delete/')
def delete_profile():

  if not current_user.is_active:
    return redirect(url_for('auth.login'))

  user = User.query.filter_by(id=current_user.id).first()

  db.session.delete(user)
  db.session.commit()

  logout_user()

  return redirect(url_for('home.index_view'))
