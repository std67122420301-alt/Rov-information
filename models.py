from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)


class Hero(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50))

    role = db.Column(db.String(50))

    image = db.Column(db.String(200))

    difficulty = db.Column(db.Integer)

    hp = db.Column(db.Integer)

    attack = db.Column(db.Integer)

    defense = db.Column(db.Integer)

    speed = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))