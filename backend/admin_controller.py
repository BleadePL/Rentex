from flask import request
from flask_login import login_required

from backend.models import Car, Location
from database_access import RENTAL_DB
from flask_main import app, BAD_REQUEST, EMPTY_OK
from utils import parse_required_fields, is_latitude_valid, is_longitude_valid


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
