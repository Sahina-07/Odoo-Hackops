from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    vehicle_type = db.Column(db.String(50))
    capacity = db.Column(db.Float)
    odometer = db.Column(db.Float)
    cost = db.Column(db.Float)
    status = db.Column(db.String(20), default="Available")


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    license_number = db.Column(db.String(100), unique=True)
    category = db.Column(db.String(20))
    expiry = db.Column(db.String(20))
    contact = db.Column(db.String(20))
    safety_score = db.Column(db.Float)
    status = db.Column(db.String(20), default="Available")


class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(100))
    destination = db.Column(db.String(100))
    cargo = db.Column(db.Float)
    distance = db.Column(db.Float)
    status = db.Column(db.String(20), default="Draft")


class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle = db.Column(db.String(50))
    description = db.Column(db.String(200))
    cost = db.Column(db.Float)
    status = db.Column(db.String(20))


class Fuel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle = db.Column(db.String(50))
    liters = db.Column(db.Float)
    amount = db.Column(db.Float)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle = db.Column(db.String(50))
    expense_type = db.Column(db.String(50))
    amount = db.Column(db.Float)