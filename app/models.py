from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    password = db.Column(db.String(128))

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.admin = False

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
