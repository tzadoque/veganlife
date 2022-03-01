from datetime import timedelta

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app import db
from app.models import User
from app.forms import LoginForm, RegisterForm

def init_app(app):

  @app.route("/")
  def index():
    # users = User.query.all() # Select * from users
    if current_user.is_active:
      return render_template("home.html")
    return render_template("landing-page.html")

  @app.route("/user/delete/<int:id>")
  def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()

    return redirect("/")

  @app.route("/register", methods=["GET", "POST"])
  def register():
    form = RegisterForm()

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

  @app.route("/login", methods=["GET", "POST"])
  def login():
    form = LoginForm()

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

  @app.route("/produtos")
  def produtos():
    return render_template("produtos.html")

  @app.route("/profile")
  def profile():
    return render_template("profile.html")