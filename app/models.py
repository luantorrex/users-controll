from app import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    admin = db.Column(db.Boolean)
    password = db.Column(db.String(30))

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
