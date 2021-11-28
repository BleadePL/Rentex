from flask import request
from flask_login import login_required

from backend.models import Car, Location
from database_access import RENTAL_DB
from flask_main import app, BAD_REQUEST
from utils import parse_required_fields, is_latitude_valid, is_longitude_valid


@app.route("/browse/nearestcars", methods=["GET"])
@login_required
def getNearestCars():
    print(request.args["locationLat"])
    fields = parse_required_fields(request.args, ["locationLat", "locationLong"])
    if fields is None:
        return BAD_REQUEST
    if "distance" in request.args:
        fields["distance"] = request.args["distance"]
    else:
        fields["distance"] = 500
    if not is_latitude_valid(fields["locationLat"]) or not is_longitude_valid(fields["locationLong"]):
        return BAD_REQUEST
    if fields["distance"] > 2000:
        fields["distance"] = 2000
    if fields["distance"] < 100:
        fields["distance"] = 100
    cars = RENTAL_DB.browseNearestCars((fields["locationLat"], fields["locationLong"]), fields["distance"])
    carsDicts = list(map(lambda d: d.to_dict_with_less_details(), cars))
    return {"cars": carsDicts}, 200


@app.route("/browse/nearestlocations", methods=["GET"])
@login_required
def getNearestLocations():
    if request.json is None:
        return BAD_REQUEST
    fields = parse_required_fields(request.json, ["locationLat", "locationLong", "distance"])
    if fields is None or not is_latitude_valid(fields["locationLat"]) or not is_longitude_valid(fields["locationLong"]):
        return BAD_REQUEST
    if fields["distance"] > 2000:
        fields["distance"] = 2000
    if fields["distance"] < 100:
        fields["distance"] = 100
    cars = RENTAL_DB.browseNearestLocations((fields["locationLat"], fields["locationLong"]), fields["distance"])
    carsDicts = list(map(lambda d: d.to_dict_with_less_details(), cars))
    return {"locations": carsDicts}


@app.route("/browse/car/<car_id>", methods=["GET"])
@login_required
def getCar(car_id: str):
    car: Car = RENTAL_DB.getCar(car_id)
    if car is None:
        return BAD_REQUEST
    return car.to_dict_with_less_details()


@app.route("/browse/location/<location_id>", methods=["GET"])
@login_required
def getLocation(location_id: str):
    location: Location = RENTAL_DB.getLocation(location_id)
    if location is None:
        return BAD_REQUEST
    return location
