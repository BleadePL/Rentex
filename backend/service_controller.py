from flask import request, Response, Request
from flask_login import login_user, logout_user, login_required, current_user

from backend.models import Location
from database_access import RENTAL_DB
from flask_main import app, login, EMPTY_OK, BAD_REQUEST

from utils import parse_required_fields, calculate_gps_distance


@app.route("/service", methods=["POST"])
@login_required
def startService():
    if request.json is None:
        return BAD_REQUEST
    parsed = parse_required_fields(request.json, ["carId"])
    if parsed is None:
        return BAD_REQUEST
    if "desc" in request.json:
        parsed["desc"] = request.json["desc"]
    else:
        parsed["desc"] = "Rutynowa kontrola"

    car = RENTAL_DB.getCar(parsed["carId"])
    l = RENTAL_DB.browseNearestLocations((car.currentLocationLat, car.currentLocationLong), 10000)  # TODO
    l.sort(key=lambda d: calculate_gps_distance((float(car.currentLocationLat), float(car.currentLocationLong)),
                                                (float(d.locationLat), float(d.locationLong))))
    loc: Location = l[0]
    if loc is None:
        return BAD_REQUEST
    id = RENTAL_DB.serviceCar(parsed["carId"], current_user.get_id(), loc._id, "Serwis 1234")
    if id is None:
        return BAD_REQUEST
    return {"serviceId": id}, 200


@app.route("/service/<service_id>", methods=["GET"])
@login_required
def getService(service_id: str):
    s = RENTAL_DB.getService(service_id)
    if s is None:
        return {}, 204
    return s, 200


@app.route("/service/<service_id>", methods=["DELETE"])
@login_required
def deleteService(service_id: str):
    ser = RENTAL_DB.getService(service_id)
    if ser is None:
        return BAD_REQUEST
    if RENTAL_DB.endService(ser):
        return EMPTY_OK
    else:
        return BAD_REQUEST


@app.route("/service/car/<car_id>", methods=["GET"])
@login_required
def getServices(car_id: str):
    return {"services": RENTAL_DB.getServicesHistory(car_id)}, 200
