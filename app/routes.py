from app import app, db
from app.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user
from flask_login import current_user
from app.models import User


@app.route('/', methods=["GET", "POST"])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for("user"))
        else:
            flash("Usuário ou senha incorretos!")
    if current_user.is_authenticated:
        return render_template("user.html")
    return render_template("home.html", form=form)


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if username is None and email is None:
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Validado e cadastrado!")
        if username is not None:
            flash("Username already in use. Please choose another one.")
        if email is not None:
            flash("Email already in use. Please choose another one.")
    return render_template("signup.html", form=form)


@app.route('/user/')
@login_required
def user():
    return render_template("user.html")


@app.route('/changeemail/', methods=["GET", "POST"])
def changeEmail():
    return render_template("changeemail.html")


@app.route('/changepassword/', methods=["GET", "POST"])
def changePassword():
    return render_template("changepassword.html")


@app.route('/confirmAdmin/', methods=["GET", "POST"])
def confirmAdmin():
    return render_template("confirm-admin.html")


"""
@app.route('/view/<password>/')
def view(password):
    if password == 'pass123' and session.permanent is True:
        return render_template("view.html", values=users.query.all())
    return redirect(url_for("home"))
"""


@app.route('/signout/')
def signout():
    logout_user()
    return redirect(url_for("home"))
