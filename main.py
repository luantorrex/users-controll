from flask import Flask, request, render_template, redirect, url_for, session
from flask import flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes=2)

db = SQLAlchemy(app)


class users(db.Model):
    _id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(30))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


@app.route('/')
def home():
    if session.permanent is True:
        return redirect(url_for("user"))
    return render_template("home.html")


def isEmailInUse(emailToValidate):
    exists = db.session.query(users._id).filter_by(
        email=emailToValidate).scalar() is not None
    return exists


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session["fullname"] = request.form["fullname"]
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        exists = isEmailInUse(request.form["email"])

        if exists:
            flash("This email address is already in use.")
            return redirect(url_for("signup"))
        else:
            session.permanent = True
            user = users(
                session["fullname"], session["email"], session["password"])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user"))
    if request.method == "GET":
        if session.permanent is True:
            return redirect(url_for("user"))
        return render_template("signup.html")


@app.route('/user/')
def user():
    if session.permanent is True:
        return render_template("user.html")
    return redirect(url_for("home"))


@app.route('/changeemail/', methods=["GET", "POST"])
def changeEmail():
    if request.method == "POST":
        emailFromInput = request.form["email"]
        if isEmailInUse(emailFromInput):
            flash("This email is already in use")
            return redirect(url_for("changeEmail"))
        else:
            session["email"] = emailFromInput
            flash("You have successfully changed your email.", "info")
            return redirect(url_for("user"))
    else:
        if "fullname" in session:
            return render_template("changeemail.html")
        else:
            return redirect(url_for("home"))


@app.route('/changepassword/', methods=["GET", "POST"])
def changePassword():
    if request.method == "POST":
        session["password"] = request.form["password"]
        flash("You have successfully changed your password.", "info")
        return redirect(url_for("user"))
    else:
        if "fullname" in session:
            return render_template("changepassword.html")
        else:
            return redirect(url_for("home"))


@app.route('/confirmAdmin/', methods=["GET", "POST"])
def confirmAdmin():
    if request.method == "POST":
        if request.form["password"] == 'pass123':
            return redirect(url_for("view", password='pass123'))
        else:
            flash("Wrong Password!")
            return render_template("confirm-admin.html")
    else:
        if session.permanent is True:
            return render_template("confirm-admin.html")
        return redirect(url_for("home"))


@app.route('/view/<password>/')
def view(password):
    if password == 'pass123' and session.permanent is True:
        return render_template("view.html", values=users.query.all())
    return redirect(url_for("home"))


@app.route('/signout/')
def signout():
    if session.permanent is True:
        session.pop("fullname", None)
        session.pop("email", None)
        session.pop("password", None)
        session.permanent = False
        flash("You have been logout.", "info")
    else:
        flash("You was not logged in")
    return redirect(url_for("home"))


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
