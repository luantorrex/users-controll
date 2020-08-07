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
    if "fullname" in session:
        return redirect(url_for("user"))
    return render_template("home.html")


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session.permanent = True
        session["fullname"] = request.form["fullname"]
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        user = users(
            session["fullname"],
            session["email"],
            session["password"])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user"))
    if request.method == "GET":
        return render_template("signup.html")


@app.route('/user/')
def user():
    return render_template("user.html")


@app.route('/changeemail/', methods=["GET", "POST"])
def changeemail():
    if request.method == "POST":
        session["email"] = request.form["email"]
        flash("You have successfully changed your email.", "info")
        return redirect(url_for("user"))
    else:
        if "fullname" in session:
            return render_template("changeemail.html")
        else:
            return render_template("home.html")


@app.route('/changepassword/', methods=["GET", "POST"])
def changepassword():
    if request.method == "POST":
        session["password"] = request.form["password"]
        flash("You have successfully changed your password.", "info")
        return redirect(url_for("user"))
    else:
        if "fullname" in session:
            return render_template("changepassword.html")
        else:
            return render_template("home.html")


@app.route('/signout/')
def signout():
    session.pop("fullname", None)
    session.pop("email", None)
    session.pop("password", None)
    flash("You have been logout.", "info")
    return redirect(url_for("home"))


@app.route('/view/')
def view():
    return render_template("view.html", values=users.query.all())


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
