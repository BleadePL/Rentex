from flask import request
from flask_login import login_required

from backend.models import Car, Location
from database_access import RENTAL_DB
from flask_main import app, BAD_REQUEST, EMPTY_OK
from utils import parse_required_fields, is_latitude_valid, is_longitude_valid


@app.route("/admin/car", methods=["POST"])
def addNewCar():
    pass


@app.route("/admin/car", methods=["GET"])
def getCars():
    pass


@app.route("/admin/car/<car_id>", methods=["GET"])
def getCarDetails(car_id):
    pass


@app.route("/admin/car/<car_id>", methods=["DELETE"])
def deleteCar(car_id):
    pass


@app.route("/admin/car/<car_id>", methods=["PATCH"])
def patchCar(car_id):
    pass


@app.route("/admin/car/<car_id>/rentalhistory", methods=["GET"])
def rentalHistory(car_id):
    pass


@app.route("/admin/user", methods=["GET"])
def getUsersList():
    pass


@app.route("/admin/user/<user_id>", methods=["GET"])
def getUserDetails(user_id):
    pass


@app.route("/admin/user/<user_id>", methods=["DELETE"])
def deleteUser(user_id):
    pass


@app.route("/admin/user/<user_id>", methods=["PATCH"])
def patchUser(user_id):
    pass


@app.route("/admin/user/<user_id>/activate", methods=["POST"])
def activateUser(user_id):
    pass


@app.route("/admin/user/<user_id>/documents", methods=["GET"])
def getDocuments(user_id):
    pass


@app.route("/admin/user/<user_id>/documents", methods=["DELETE"])
def denyDocuments(user_id):
    pass


@app.route("/admin/user/<user_id>/documents", methods=["PUT"])
def acceptDocuments(user_id):
    pass


@app.route("/admin/user/<user_id>/rentalhistory", methods=["GET"])
def getRentalHistory(user_id):
    pass


@app.route("/admin/location", methods=["POST"])
def addNewLocation():
    pass


@app.route("/admin/location", methods=["GET"])
def getLocations():
    pass


@app.route("/admin/location/<location_id>", methods=["GET"])
def getLocationDetails(location_id):
    pass


@app.route("/admin/location/<location_id>", methods=["DELETE"])
def deleteLocation(location_id):
    pass


@app.route("/admin/location/<location_id>", methods=["PATCH"])
def patchLocation(location_id):
    pass


@app.route("/admin/carpos", methods=["POST"])
def setCarPos():
    if request.json is None:
        return BAD_REQUEST
    parse = parse_required_fields(request.json, ["carid", "long", "lat"])
    if parse is None:
        return BAD_REQUEST
    if RENTAL_DB.patchCar(parse["carid"], {'currentLocationLat': parse["lat"], 'currentLocationLong': parse["long"]}):
        return EMPTY_OK
    else:
        return BAD_REQUEST


@app.route("/admin/activateuser", methods=["POST"])
def activateUser():
    if request.json is None:
        return BAD_REQUEST
    parse = parse_required_fields(request.json, ["userid"])
    if parse is None:
        return BAD_REQUEST
    if RENTAL_DB.acceptDocuments(parse["userid"]):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/deleteaccount", methods=["DELETE"])
def deleteAccount():
    if request.json is None:
        return BAD_REQUEST
    parse = parse_required_fields(request.json, ["userid"])
    if parse is None:
        return BAD_REQUEST

    if RENTAL_DB.deleteUser(parse["userid"]):
        return EMPTY_OK
    return BAD_REQUEST
