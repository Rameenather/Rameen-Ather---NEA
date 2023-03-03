from __init__ import db
from flask_login import UserMixin
from sqlalchemy.sql import func




class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    status = db.Column(db.String(150))


class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_email = db.Column(db.String(150), nullable = False)
    student_name = db.Column(db.String(150), nullable = False)
    taught = db.Column(db.String(150), nullable = False)
    date_entered = db.Column(db.DateTime(timezone = True), default = func.now())
    teacher = db.Column(db.Integer, db.ForeignKey('user.id',ondelete = "CASCADE"), nullable = False)
