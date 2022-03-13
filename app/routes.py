import mimetypes
import os
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.config import Config
from app.models.User import User
from app.models.Product import Product
from app.forms import LoginUser, RegisterUser

def init_app(app):

  @app.route("/")
  def index():
    if current_user.is_active:
      return render_template("home.html")
    return render_template("landing-page.html")

  @app.route("/user/delete/<int:id>")
  def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

  @app.route("/register/", methods=("GET", "POST"))
  def register():
    form = RegisterUser()

    if form.validate_on_submit():

      user = User()

      if form.password.data != form.repeat_password.data:
        flash("As senhas precisam ser iguais", category="danger")
        return redirect(url_for("register"))

      if User.query.filter_by(email=form.email.data).first():
        flash("O email já está registrado", category="danger")
        return redirect(url_for("register"))
      
      user.name = form.name.data
      user.last_name = form.last_name.data
      user.birth_date = form.birth_date.data
      user.email = form.email.data
      user.password = generate_password_hash(form.password.data)

      db.session.add(user)
      db.session.commit()

      login_user(user)
      return redirect(url_for("index"))

    return render_template("register.html", form=form)

  @app.route("/login/", methods=("GET", "POST"))
  def login():
    form = LoginUser()

    if form.validate_on_submit():
      user = User.query.filter_by(email=form.email.data).first()

      if not user:
        flash("Email incorreto", category="danger")
        return redirect(url_for("login"))

      if not check_password_hash(user.password, form.password.data):
        flash("Email correto", category="success")
        flash("Senha incorreta", category="danger")
        return redirect(url_for("login"))

      login_user(user)
      return redirect(url_for("index"))

    return render_template("login.html", form=form)

  @app.route("/logout")
  @login_required
  def logout():
    logout_user()
    return redirect(url_for("index"))

  @app.route("/profile/")
  def profile():

    if not current_user.is_active:
      return redirect(url_for('login'))

    user = User.query.filter_by(id=current_user.id).first()

    day = user.birth_date[8] + user.birth_date[9]
    month = user.birth_date[5] + user.birth_date[6] 
    year = user.birth_date[0] + user.birth_date[1] + user.birth_date[2] + user.birth_date[3]

    formated_birth_date = f'{day}/{month}/{year}'

    return render_template("profile.html", user=user, formated_birth_date=formated_birth_date)
  
  @app.route("/profile/edit", methods=("GET", "POST"))
  def edit_profile():

    if not current_user.is_active:
      return redirect(url_for('login'))
    
    form = RegisterUser()

    user = User.query.filter_by(id=current_user.id).first()

    form.name.data = user.name
    form.last_name.data = user.last_name
    form.email.data = user.email

    return render_template("edit_profile.html", user=user, form=form)

  @app.route("/profile/edit/submit", methods=("GET", "POST"))
  def submit_profile_edit():
    
    if not current_user.is_active:
      return redirect(url_for('login'))

    form = RegisterUser()

    user = User.query.filter_by(id=current_user.id).first()

    if form.validate_on_submit():

      if User.query.filter_by(email=form.email.data).first():
        if form.email.data != user.email:
          flash("O email já está registrado", category="danger")
          return redirect(url_for("edit_profile"))

      user.name = form.name.data
      user.last_name = form.last_name.data
      user.birth_date = form.birth_date.data
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

      return redirect(url_for('profile'))


  @app.route("/produtos/")
  def produtos():

    if current_user.is_active:
      products = Product.query.all()
      return render_template("produtos.html", products=products)
    
    return redirect(url_for('login'))

  @app.route("/produtos/<int:id>/")
  def produto(id):

    if current_user.is_active:
      product = Product.query.filter_by(id=id).first()
      return render_template("produto.html", product=product)

    return redirect(url_for('login'))

  @app.errorhandler(404)
  def page_not_found(e):
    return render_template('404.html'), 404