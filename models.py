from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# =========================
# Vehicle
# =========================

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    registration = db.Column(db.String(20), unique=True, nullable=False)

    name = db.Column(db.String(100), nullable=False)

    vehicle_type = db.Column(db.String(50), nullable=False)

    capacity = db.Column(db.Float, nullable=False)

    odometer = db.Column(db.Float, default=0)

    acquisition_cost = db.Column(db.Float, default=0)

    status = db.Column(db.String(20), default="Available")


# =========================
# Driver
# =========================

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    license_number = db.Column(db.String(50), unique=True, nullable=False)

    license_category = db.Column(db.String(50))

    license_expiry = db.Column(db.Date)

    contact = db.Column(db.String(20))

    safety_score = db.Column(db.Float, default=100)

    status = db.Column(db.String(20), default="Available")


# =========================
# Trip
# =========================

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    source = db.Column(db.String(100))

    destination = db.Column(db.String(100))

    cargo_weight = db.Column(db.Float)

    planned_distance = db.Column(db.Float)

    revenue = db.Column(db.Float)

    status = db.Column(db.String(20), default="Dispatched")

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


# =========================
# Maintenance
# =========================

class Maintenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicle.id")
    )

    description = db.Column(db.String(200))

    cost = db.Column(db.Float)

    status = db.Column(db.String(20), default="Open")

    vehicle = db.relationship("Vehicle")


# =========================
# Fuel Log
# =========================

class FuelLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(
        db.Integer,
        db.ForeignKey("vehicle.id")
    )

    liters = db.Column(db.Float)

    cost = db.Column(db.Float)

    date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    vehicle = db.relationship("Vehicle")


# =========================
# Expense
# =========================

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(100))

    amount = db.Column(db.Float)

    date = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )