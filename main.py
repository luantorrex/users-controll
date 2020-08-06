from flask import Flask, request, render_template, redirect, url_for, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "hello"

@app.route('/')
def home():
    return render_template("home.html")
    
@app.route('/user/')
def user():
    return render_template("user.html")

@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        session["fullname"] = request.form["fullname"]
        session["email"] = request.form["email"]
        session["password"] = request.form["password"]
        return redirect(url_for("user"))
    if request.method == "GET":
        return render_template("signup.html")

@app.route('/signout/')
def signout():
    session.pop("fullname", None)
    session.pop("email", None)
    session.pop("password", None)
    return redirect(url_for("home"))

app.run(debug= True)