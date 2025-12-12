from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password, pwd)

class Bus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    source = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    seats = db.Column(db.Integer)
    price = db.Column(db.Float)

class Train(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    source = db.Column(db.String(200))
    destination = db.Column(db.String(200))
    seats = db.Column(db.Integer)
    price = db.Column(db.Float)

# class Booking(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user = db.Column(db.String(200))
#     transport_type = db.Column(db.String(50))
#     transport_name = db.Column(db.String(200))
#     source = db.Column(db.String(200))
#     destination = db.Column(db.String(200))
#     seats = db.Column(db.Integer)
#     total_price = db.Column(db.Float)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    transport_type = db.Column(db.String(20))
    transport_name = db.Column(db.String(100))
    source = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    seats = db.Column(db.Integer)
    total_price = db.Column(db.Integer)
    status = db.Column(db.String(20), default="Booked")  # NEW FIELD


