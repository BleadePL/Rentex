from flask import request, Response, Request
from flask_login import login_user, logout_user, login_required, current_user

from backend.db_interface import DatabaseInterface
from database_access import RENTAL_DB
from flask_main import app, login, EMPTY_OK, BAD_REQUEST

from utils import parse_required_fields


@app.route("/service", methods=["POST"])
@login_required
def startService():
    if request.json is None:
        return BAD_REQUEST
    parsed = parse_required_fields(request.json, ["carId"])
    if parsed is None:
        return BAD_REQUEST
    id = RENTAL_DB.serviceCar(parsed["carId"])
    if id is None:
        return BAD_REQUEST
    return {"serviceId": id}, 200


@app.route("/service/<service_id>", methods=["GET"])
@login_required
def getService(service_id: str):
    s = RENTAL_DB.getService(service_id)
    if s is None:
        return BAD_REQUEST
    return s, 200


@app.route("/service/<service_id>", methods=["DELETE"])
@login_required
def deleteService(service_id: str):
    if RENTAL_DB.endService(service_id):
        return EMPTY_OK
    else:
        return BAD_REQUEST


@app.route("/service/car/<car_id>", methods=["GET"])
@login_required
def getServices(car_id: str):
    return RENTAL_DB.getServicesHistory(car_id), 200
