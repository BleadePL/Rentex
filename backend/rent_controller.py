from flask import request
from flask_login import login_required, current_user

from database_access import RENTAL_DB
from flask_main import app, EMPTY_OK, BAD_REQUEST, rental_timer_task, PendingRental
from utils import parse_required_fields, gr_to_pln_gr


@app.route("/rent/reservation/<reservation_id>", methods=["GET"])
@login_required
def getReservation(reservation_id: str):
    res = RENTAL_DB.getReservation(current_user.get_id(), reservation_id)
    if res is None:
        return BAD_REQUEST
    return {"reservation": res.__dict__}, 200


@app.route("/rent/reservation/<reservation_id>", methods=["DELETE"])
@login_required
def deleteReservation(reservation_id: str):
    if rental_timer_task.endReservation(reservation_id):
        return EMPTY_OK
    else:
        return BAD_REQUEST


@app.route("/rent/reservate", methods=["GET"])
@login_required
def getReservationOfUser():
    user = RENTAL_DB.getUser(current_user.get_id())
    if user is None:
        return BAD_REQUEST
    if user.reservation is None:
        return {}, 204
    return {"reservation": user.reservation}, 200

@app.route("/rent/reservate", methods=["POST"])
@login_required
def reservate():
    if request.json is None or "carId" not in request.json:
        return BAD_REQUEST
    resId = rental_timer_task.startReservation(car_id=request.json["carId"], user_id=current_user.get_id())
    if resId is None:
        return BAD_REQUEST
    return {"resId": resId}, 200


@app.route("/rent/rent", methods=["GET"])
@login_required
def getRentOfUser():
    user = RENTAL_DB.getUser(current_user.get_id())
    if user is None:
        return BAD_REQUEST
    if user.currentRental is None or user.currentRental == "":
        return {}, 204
    pending: PendingRental = rental_timer_task.getRental(user.currentRental["_id"])
    if pending is not None:
        r = user.currentRental.copy()
        r["mileage"] = pending.distance
        r["totalCost"] = gr_to_pln_gr(pending.calculate_current_cost())
        return {"rental": r}
    return {"rental": user.currentRental}, 200


@app.route("/rent/rent", methods=["POST"])
@login_required
def rent():
    if request.json is None:
        return BAD_REQUEST
    parsed = parse_required_fields(request.json, ["carId", "paymentType"])
    if parsed is None:
        return BAD_REQUEST
    car = RENTAL_DB.getCar(parsed["carId"])
    if car is None:
        return BAD_REQUEST
    if parsed["paymentType"] != "PP":
        if "cvv" not in request.json:
            return BAD_REQUEST
        creditCard = RENTAL_DB.getCard(current_user.get_id(), cardId=parsed["paymentType"])
        if creditCard is None:
            return BAD_REQUEST
        pp = "CC"
        parsed["cvv"] = request.json["cvv"]
    else:
        creditCard = None
        pp = "PP"
        parsed["cvv"] = 0

    rent_id = rental_timer_task.rent(car, current_user.get_id(), pp, parsed["cvv"], creditCard)
    if rent_id is None:
        return BAD_REQUEST
    else:
        return {"rentId": rent_id}, 200


@app.route("/rent/rent/<rent_id>", methods=["GET"])
@login_required
def getRent(rent_id):
    rental: PendingRental = rental_timer_task.getRental(rent_id)
    if rental is not None:
        if rental.rent.renter != current_user.get_id():
            return BAD_REQUEST
        d = rental.rent.__dict__.copy()
        d["mileage"] = rental.distance
        d["totalCost"] = gr_to_pln_gr(rental.calculate_current_cost())
        return {"rental": d}, 200
    r = RENTAL_DB.getRental(current_user.get_id(), rentalId=rent_id)
    if r is None:
        return BAD_REQUEST
    return {"rental": r.__dict__}, 200


@app.route("/rent/rent/<rent_id>", methods=["DELETE"])
@login_required
def finishRent(rent_id):
    if not rental_timer_task.endRent(rent_id):
        return BAD_REQUEST
    return EMPTY_OK
