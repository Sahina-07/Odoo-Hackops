from flask import Flask, render_template, request, redirect, flash
from models import db, Vehicle

app = Flask(__name__)

app.config["SECRET_KEY"] = "TransitOps123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return redirect("/dashboard")


@app.route("/dashboard")
def dashboard():
    vehicles = Vehicle.query.all()
    return render_template("dashboard.html", vehicles=vehicles)


@app.route("/vehicles")
def vehicles():
    vehicles = Vehicle.query.all()
    return render_template("vehicles.html", vehicles=vehicles)


@app.route("/add_vehicle", methods=["POST"])
def add_vehicle():

    reg = request.form["registration"]

    existing = Vehicle.query.filter_by(registration=reg).first()

    if existing:
        flash("Registration already exists!")
        return redirect("/vehicles")

    vehicle = Vehicle(
        registration=reg,
        name=request.form["name"],
        vehicle_type=request.form["vehicle_type"],
        capacity=request.form["capacity"],
        odometer=request.form["odometer"],
        acquisition_cost=request.form["cost"],
        status=request.form["status"]
    )

    db.session.add(vehicle)
    db.session.commit()

    flash("Vehicle Added Successfully")

    return redirect("/vehicles")


if __name__ == "__main__":
    app.run(debug=True)