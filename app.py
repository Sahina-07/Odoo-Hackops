<<<<<<< HEAD
from flask import Flask, render_template, request, redirect, flash
from models import db, Vehicle, Driver, Trip, Maintenance, FuelLog, Expense

app = Flask(__name__)

app.config["SECRET_KEY"] = "TransitOps123"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------- HOME ---------------- #

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():

    active_vehicles = Vehicle.query.count()

    active_drivers = Driver.query.count()

    trips = Trip.query.count()

    maintenance = Maintenance.query.count()

    return render_template(
        "dashboard.html",
        active_vehicles=active_vehicles,
        active_drivers=active_drivers,
        trips=trips,
        maintenance=maintenance
    )


# ---------------- VEHICLES ---------------- #

@app.route("/vehicles")
def vehicles():

    vehicles = Vehicle.query.all()

    return render_template("vehicles.html", vehicles=vehicles)
=======
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
>>>>>>> 63c673cbe32fb494f642f9b5033403652b5a95b2

    name = db.Column(db.String(100), nullable=False)

    vehicle_type = db.Column(db.String(50), nullable=False)

    capacity = db.Column(db.Float, nullable=False)

    odometer = db.Column(db.Float, default=0)

<<<<<<< HEAD
    if existing:
        flash("Registration Number already exists!")
        return redirect("/vehicles")

    vehicle = Vehicle(
        registration=reg,
        name=request.form["name"],
        vehicle_type=request.form["vehicle_type"],
        capacity=request.form["capacity"],
        odometer=request.form["odometer"],
        acquisition_cost=request.form["acquisition_cost"],
        status=request.form["status"]
=======
    acquisition_cost = db.Column(db.Float, default=0)

    status = db.Column(
        db.String(20),
        default="Available"
>>>>>>> 63c673cbe32fb494f642f9b5033403652b5a95b2
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


<<<<<<< HEAD
# ---------------- DRIVERS ---------------- #

@app.route("/drivers")
def drivers():

    drivers = Driver.query.all()

    return render_template("drivers.html", drivers=drivers)


# ---------------- TRIPS ---------------- #

@app.route("/trips")
def trips():

    trips = Trip.query.all()

    vehicles = Vehicle.query.filter_by(status="Available").all()

    drivers = Driver.query.filter_by(status="Available").all()

    return render_template(
        "trips.html",
        trips=trips,
        vehicles=vehicles,
        drivers=drivers
    )


# ---------------- MAINTENANCE ---------------- #

@app.route("/maintenance")
def maintenance():

    maintenance = Maintenance.query.all()

    vehicles = Vehicle.query.all()

    return render_template(
        "maintenance.html",
        maintenance=maintenance,
        vehicles=vehicles
    )


# ---------------- FUEL ---------------- #

@app.route("/fuel")
def fuel():

    logs = FuelLog.query.all()

    vehicles = Vehicle.query.all()

    return render_template(
        "fuel.html",
        logs=logs,
        vehicles=vehicles
    )


# ---------------- REPORTS ---------------- #

@app.route("/reports")
def reports():

    vehicles = Vehicle.query.all()

    drivers = Driver.query.all()

    trips = Trip.query.all()

    return render_template(
        "reports.html",
        vehicles=vehicles,
        drivers=drivers,
        trips=trips
    )

# ---------------- ADD DRIVER ---------------- #

@app.route("/add_driver", methods=["POST"])
def add_driver():

    driver = Driver(

        name=request.form["name"],

        license_number=request.form["license_number"],

        license_category=request.form["license_category"],

        license_expiry=request.form["license_expiry"],

        contact=request.form["contact"],

        safety_score=request.form["safety_score"],

        status=request.form["status"]

    )

    db.session.add(driver)

    db.session.commit()

    flash("Driver Added Successfully")

    return redirect("/drivers")


# ---------------- ADD TRIP ---------------- #

@app.route("/add_trip", methods=["POST"])
def add_trip():

    vehicle = Vehicle.query.get(request.form["vehicle_id"])

    driver = Driver.query.get(request.form["driver_id"])


    if vehicle.status != "Available":

        flash("Vehicle Not Available")

        return redirect("/trips")


    if driver.status != "Available":

        flash("Driver Not Available")

        return redirect("/trips")


    if float(request.form["cargo_weight"]) > vehicle.capacity:

        flash("Cargo exceeds Vehicle Capacity")

        return redirect("/trips")


    trip = Trip(

        source=request.form["source"],

        destination=request.form["destination"],

        cargo_weight=request.form["cargo_weight"],

        planned_distance=request.form["planned_distance"],

        revenue=request.form["revenue"],

        vehicle_id=vehicle.id,

        driver_id=driver.id,

        status="Dispatched"

    )

    vehicle.status = "On Trip"

    driver.status = "On Trip"

    db.session.add(trip)

    db.session.commit()

    flash("Trip Created Successfully")

    return redirect("/trips")

# ---------------- ADD MAINTENANCE ---------------- #

@app.route("/add_maintenance", methods=["POST"])
def add_maintenance():

    vehicle = Vehicle.query.get(request.form["vehicle_id"])

    maintenance = Maintenance(
        vehicle_id=vehicle.id,
        description=request.form["description"],
        cost=float(request.form["cost"]),
        status="Open"
    )

    vehicle.status = "In Shop"

    db.session.add(maintenance)
    db.session.commit()

    flash("Maintenance Record Added")

    return redirect("/maintenance")


# ---------------- CLOSE MAINTENANCE ---------------- #

@app.route("/close_maintenance/<int:id>")
def close_maintenance(id):

    maintenance = Maintenance.query.get(id)

    if maintenance:

        maintenance.status = "Completed"

        vehicle = Vehicle.query.get(maintenance.vehicle_id)

        if vehicle.status != "Retired":
            vehicle.status = "Available"

        db.session.commit()

    flash("Maintenance Closed")

    return redirect("/maintenance")


# ---------------- ADD FUEL ---------------- #

@app.route("/add_fuel", methods=["POST"])
def add_fuel():

    fuel = FuelLog(

        vehicle_id=request.form["vehicle_id"],

        liters=float(request.form["liters"]),

        cost=float(request.form["cost"])

    )

    db.session.add(fuel)

    db.session.commit()

    flash("Fuel Log Added")

    return redirect("/fuel")


# ---------------- COMPLETE TRIP ---------------- #

@app.route("/complete_trip/<int:id>")
def complete_trip(id):

    trip = Trip.query.get(id)

    if trip:

        trip.status = "Completed"

        vehicle = Vehicle.query.get(trip.vehicle_id)

        driver = Driver.query.get(trip.driver_id)

        vehicle.status = "Available"

        driver.status = "Available"

        db.session.commit()

    flash("Trip Completed")

    return redirect("/trips")


# ---------------- CANCEL TRIP ---------------- #

@app.route("/cancel_trip/<int:id>")
def cancel_trip(id):

    trip = Trip.query.get(id)

    if trip:

        trip.status = "Cancelled"

        vehicle = Vehicle.query.get(trip.vehicle_id)

        driver = Driver.query.get(trip.driver_id)

        vehicle.status = "Available"

        driver.status = "Available"

        db.session.commit()

    flash("Trip Cancelled")

    return redirect("/trips")

if __name__ == "__main__":
    app.run(debug=True)
=======
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
>>>>>>> 63c673cbe32fb494f642f9b5033403652b5a95b2
