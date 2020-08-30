from app import db


class User(db.Model):
    _id = db.Column("id", db.Integer(), primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(30))

    def __repr__(self):
        return '<User %r>' % self.username
