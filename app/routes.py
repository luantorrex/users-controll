from app import app, db
from app.forms import ChangeEmail, ChangePassword, RegistrationForm, LoginForm
from app.forms import AdminCheck
from app.models import User
from flask import render_template, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user
from flask_login import current_user


@app.route('/', methods=["GET", "POST"])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
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
                        email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Congratulations! You just created your account")
            return redirect(url_for("user"))
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
@login_required
def changeEmail():
    form = ChangeEmail()
    newEmail = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit() and newEmail is None:
        current_user.email = form.email.data
        db.session.add(current_user)
        db.session.commit()
        flash("E-mail changed with success.")
        return redirect(url_for("user"))
    if newEmail is not None:
        flash("E-mail already in use. Please choose another one")
    return render_template("changeemail.html", form=form)


@app.route('/changepassword/', methods=["GET", "POST"])
@login_required
def changePassword():
    form = ChangePassword()
    if form.validate_on_submit():
        current_user.set_password(form.password.data)
        db.session.add(current_user)
        db.session.commit()
        flash("Password changed with success.")
        return redirect(url_for("user"))
    return render_template("changepassword.html", form=form)


@app.route('/confirmAdmin/', methods=["GET", "POST"])
def confirmAdmin():
    form = AdminCheck()
    if form.validate_on_submit():
        if form.password.data == "pass123":
            current_user.admin = True
            db.session.add(current_user)
            db.session.commit()
            return redirect(url_for("dbView"))
        else:
            flash("Wrong password. Try Again")
    return render_template("confirm-admin.html", form=form)


@app.route('/dbView/')
@login_required
def dbView():
    if current_user.admin is True:
        return render_template("view.html", users=User.query.all())
    else:
        return redirect(url_for("confirmAdmin"))


@app.route('/changePermission/<user>', methods=["GET", "POST"])
@login_required
def changePermission(user):
    user = user.split()[-1].replace("'>", "").replace("'", "")
    user = User.query.filter_by(username=user).first()
    if user.admin is True:
        user.admin = False
        flash(user.username + " isn't an administrator anymore.")
    else:
        user.admin = True
        flash(user.username + " is an administrator now.")
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("dbView"))


@app.route('/resetPassword/<user>', methods=["GET", "POST"])
@login_required
def resetPassword(user):
    user = user.split()[-1].replace("'>", "").replace("'", "")
    user = User.query.filter_by(username=user).first()
    user.password = 'abc123'
    flash("The " + user.username + "'s password has been reset.")
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("dbView"))


@app.route('/deleteUser/<user>', methods=["GET", "POST"])
@login_required
def deleteUser(user):
    user = user.split()[-1].replace("'>", "").replace("'", "")
    user = User.query.filter_by(username=user).first()
    print(user.username, current_user.username)
    if user.username is current_user.username:
        flash("You can't delete your own account.")
        return redirect(url_for("dbView"))
    flash("The user " + user.username + " has been deleted.")
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("dbView"))


@app.route('/signout/')
def signout():
    logout_user()
    return redirect(url_for("home"))
