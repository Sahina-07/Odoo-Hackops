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


@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():

    reg = request.form["registration"]

    existing = Vehicle.query.filter_by(registration=reg).first()

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
    )

    db.session.add(vehicle)
    db.session.commit()

    flash("Vehicle Added Successfully")

    return redirect("/vehicles")


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