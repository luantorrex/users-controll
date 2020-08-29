from app import app
from app.forms import RegistrationForm
from flask import render_template, url_for, redirect, flash


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash("Validado!")
    return render_template("signup.html", form=form)


@app.route('/user/')
def user():
    return redirect(url_for("home"))


@app.route('/changeemail/', methods=["GET", "POST"])
def changeEmail():
    return render_template("changeemail.html")


@app.route('/changepassword/', methods=["GET", "POST"])
def changePassword():
    return redirect(url_for("home"))


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
    return redirect(url_for("home"))
