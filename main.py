from flask import Flask, request, render_template, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"
app.permanent_session_lifetime = timedelta(minutes=1)

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
    return redirect(url_for("home"))

app.run(debug= True)