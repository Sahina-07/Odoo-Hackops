from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()


# ---------------- USERS ---------------- #

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)


# ---------------- VEHICLES ---------------- #

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    registration = db.Column(db.String(50), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)

    vehicle_type = db.Column(db.String(50), nullable=False)

    capacity = db.Column(db.Float, nullable=False)

    odometer = db.Column(db.Float, default=0)

    acquisition_cost = db.Column(db.Float, default=0)

    status = db.Column(
        db.String(20),
        default="Available"
    )


# ---------------- DRIVERS ---------------- #

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    license_number = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    license_category = db.Column(db.String(20))

    license_expiry = db.Column(db.Date)

    contact = db.Column(db.String(20))

    safety_score = db.Column(db.Integer, default=100)

    status = db.Column(
        db.String(20),
        default="Available"
    )


# ---------------- TRIPS ---------------- #

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    source = db.Column(db.String(100))

    destination = db.Column(db.String(100))

    cargo_weight = db.Column(db.Float)

    planned_distance = db.Column(db.Float)

    revenue = db.Column(db.Float, default=0)

    status = db.Column(
        db.String(20),
        default="Draft"
    )

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicle.id")
    )

    driver_id = db.Column(
        db.Integer,
        db.ForeignKey("driver.id")
    )

    vehicle = db.relationship("Vehicle")

    driver = db.relationship("Driver")


# ---------------- MAINTENANCE ---------------- #

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicle.id")
    )

    description = db.Column(db.String(200))

    cost = db.Column(db.Float)

    status = db.Column(
        db.String(20),
        default="Open"
    )

    vehicle = db.relationship("Vehicle")


# ---------------- FUEL LOG ---------------- #

class FuelLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicle.id")
    )

    liters = db.Column(db.Float)

    cost = db.Column(db.Float)

    date = db.Column(db.Date, default=date.today)

    vehicle = db.relationship("Vehicle")


# ---------------- EXPENSES ---------------- #

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicle.id")
    )

    expense_type = db.Column(db.String(50))

    amount = db.Column(db.Float)

    date = db.Column(db.Date, default=date.today)

    vehicle = db.relationship("Vehicle")