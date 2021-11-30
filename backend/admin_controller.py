import os

from flask import request, send_file

from database_access import RENTAL_DB
from flask_main import app, BAD_REQUEST, EMPTY_OK, PHOTOS_TARGET, rental_timer_task
from utils import parse_required_fields, is_latitude_valid, is_longitude_valid


@app.route("/admin/car", methods=["POST"])
def addNewCar():
    if request.json is None:
        return BAD_REQUEST
    parse = parse_required_fields(request.json, {
        "brand", "regNumber", "model", "seats", "charge", "activationCost", "kmCost", "timeCost",
        "locationLat", "locationLong", "status", "vin", "mileage", "esimNumber", "esimImei", "regCountryCode"
    })
    if parse is None:
        return BAD_REQUEST
    if RENTAL_DB.addCar(parse):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/car", methods=["GET"])
def getCars():
    if request.args is None:
        return BAD_REQUEST
    parsed = parse_required_fields(request.args,
                                   ["locationLat", "locationLong", "pagelength", "startindex", "distance"])
    if parsed is None:
        return BAD_REQUEST
    cars = RENTAL_DB.getCars(parsed["startindex"], parsed["pagelength"],
                             (parsed["locationLat"], parsed["locationLong"]),
                             parsed["distance"])
    if cars is None:
        return BAD_REQUEST

    def getcars(car):
        d = car.__dict__
        from datetime import datetime
        for e in d:
            if type(d[e]) is datetime:
                d[e] = str(d[e])
        return d

    return {"cars": list(map(lambda car: getcars(car), cars))}, 200


@app.route("/admin/car/<car_id>", methods=["DELETE"])
def deleteCar(car_id):
    if RENTAL_DB.deleteCar(car_id):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/car/<car_id>", methods=["PATCH"])
def patchCar(car_id):
    if request.json is None:
        return BAD_REQUEST
    if RENTAL_DB.patchCar(car_id, request.json):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/user", methods=["GET"])
def getUsersList():
    parse = parse_required_fields(request.args, ["pagelength", "startindex", "filter"])
    if parse is None:
        return BAD_REQUEST
    users = RENTAL_DB.getUsers(parse["startindex"], parse["pagelength"], parse["filter"])
    return {"users": users}


@app.route("/admin/user/<user_id>", methods=["DELETE"])
def deleteUser(user_id):
    if RENTAL_DB.deleteUser(user_id):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/user/<user_id>", methods=["PATCH"])
def patchUser(user_id):
    if request.json is None:
        return BAD_REQUEST
    if RENTAL_DB.patchCar(user_id, request.json):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/user/<user_id>/activate", methods=["POST"])
def activateUser(user_id):
    if RENTAL_DB.setAccountStatus(user_id, "ACTIVE"):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/user/<user_id>/documents", methods=["GET"])
def getDocuments(user_id):
    side = request.args.get("side", "F")

    if side.lower() == "b" or side.lower() == "back":
        side = "back"
    else:
        side = "front"
    l = os.listdir(PHOTOS_TARGET)

    file = next(filter(lambda file: (user_id + "_" + side) in file, l), None)
    if file is None:
        return BAD_REQUEST
    return send_file(PHOTOS_TARGET + "/" + file, mimetype="image/png", attachment_filename=side + ".png")


@app.route("/admin/user/<user_id>/documents", methods=["DELETE"])
def denyDocuments(user_id):
    if RENTAL_DB.setAccountStatus(user_id, "PENDING"):
        l = os.listdir(PHOTOS_TARGET)
        l = list(filter(lambda file: (user_id + "_") in file, l))
        for p in l:
            os.remove(PHOTOS_TARGET + "/" + p)
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/user/<user_id>/documents", methods=["PUT"])
def acceptDocuments(user_id):
    if RENTAL_DB.setAccountStatus(user_id, "ACTIVE"):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/user/<user_id>/rentalhistory", methods=["GET"])
def getAdminRentalHistory(user_id):
    pare = parse_required_fields(request.args, ["startindex", "pagelength"])
    if pare is None:
        return BAD_REQUEST

    list = RENTAL_DB.getUserRentalHistory(user_id, pare["startindex"], pare["pagelength"])
    return {"rentals": list}, 200


@app.route("/admin/location", methods=["POST"])
def addNewLocation():
    parse = parse_required_fields(request.json,
                                  ["name", "locationLat", "locationLong", "locationType", "locationReward",
                                   "locationAddress"])
    if parse is None:
        return BAD_REQUEST
    if RENTAL_DB.addLocation(parse):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/location", methods=["GET"])
def getLocations():
    parsed = parse_required_fields(request.args,
                                   ["locationLat", "locationLong", "pagelength", "startindex", "distance"])
    if parsed is None:
        return BAD_REQUEST
    locs = RENTAL_DB.getCars(parsed["pageIndex"], parsed["pageCount"], (parsed["locationLat"], parsed["locationLong"]),
                             parsed["distance"])
    return {"locations": locs}, 200


@app.route("/admin/location/<location_id>", methods=["DELETE"])
def deleteLocation(location_id):
    if RENTAL_DB.deleteLocation(location_id):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/location/<location_id>", methods=["PATCH"])
def patchLocation(location_id):
    if request.json is None:
        return BAD_REQUEST
    if RENTAL_DB.patchLocation(location_id, request.json):
        return EMPTY_OK
    return BAD_REQUEST





# TODO: Zrobic je kiedys
@app.route("/admin/car/<car_id>", methods=["GET"])
def getCarDetails(car_id):
    pass


@app.route("/admin/location/<location_id>", methods=["GET"])
def getLocationDetails(location_id):
    pass


@app.route("/admin/car/<car_id>/rentalhistory", methods=["GET"])
def rentalHistory(car_id):
    pass


@app.route("/admin/user/<user_id>", methods=["GET"])
def getAdminUserDetails(user_id):
    u = RENTAL_DB.getUser(user_id)
    if u is None:
        return BAD_REQUEST
    u.password = "<SHADED>"
    return {"user": u.__dict__}, 200
    pass


# TODO END

@app.route("/admin/activateuser", methods=["POST"])
def adminActivateUser():
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


@app.route("/admin/carpos", methods=["POST"])
def setCarPos():
    if request.json is None:
        return BAD_REQUEST
    parse = parse_required_fields(request.json, ["carid", "long", "lat"])
    if parse is None:
        return BAD_REQUEST
    if RENTAL_DB.patchCar(parse["carid"], {'currentLocationLat': parse["lat"], 'currentLocationLong': parse["long"]}):
        rental_timer_task.updateDistance(parse["carid"], parse["lat"], parse["long"])
        return EMPTY_OK
    else:
        return BAD_REQUEST


@app.route("/admin/forcecleanreservation/<resid>/<userid>", methods=["DELETE"])
def forceCleanReservation(resid, userid):
    res = RENTAL_DB.getReservation(userid, resid)
    if res is None:
        return BAD_REQUEST
    if RENTAL_DB.endReservation(res):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/admin/forcecleanrental/<resid>/<userid>", methods=["DELETE"])
def forceCleanRental(resid, userid):
    res = RENTAL_DB.getRental(userid, resid)
    if res is None:
        return BAD_REQUEST
    if RENTAL_DB.endRental(res):
        return EMPTY_OK
    return BAD_REQUEST
