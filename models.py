"""
class users(db.Model):
    _id = db.Column("id", db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(30))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
"""
