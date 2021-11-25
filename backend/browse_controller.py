from flask import request, Response, Request
from flask_login import login_user, logout_user, login_required, current_user

from backend.db_interface import DatabaseInterface
from database_access import RENTAL_DB
from flask_main import app, login, EMPTY_OK, BAD_REQUEST


@app.route("/browse/nearestcars", methods=["GET"])
@login_required
def getNearestCars():
    pass


@app.route("/browse/nearestlocations", methods=["GET"])
@login_required
def getNearestLocations():
    pass


@app.route("/browse/car/<car_id>", methods=["GET"])
@login_required
def getCar(car_id: str):
    pass


@app.route("/browse/location/<location_id>", methods=["GET"])
@login_required
def getLocation(location_id: str):
    pass
