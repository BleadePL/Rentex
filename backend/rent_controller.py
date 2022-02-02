from flask import request
from flask_login import login_required, current_user

from backend.classes import Client, Rental
from backend.utils import row2dict
from database_access import RENTAL_DB
from flask_main import app, EMPTY_OK, BAD_REQUEST, rental_timer_task, PendingRental
from utils import parse_required_fields, gr_to_pln_gr


@app.route("/rent/reservation/<reservation_id>", methods=["GET"])
@login_required
def getReservation(reservation_id: str):
    res = RENTAL_DB.getReservation(current_user.get_id(), reservation_id)
    if res is None:
        return BAD_REQUEST
    return {"reservation": row2dict(res)}, 200


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
    reservation = RENTAL_DB.getActiveReservation(current_user.get_id())
    if reservation is None:
        return BAD_REQUEST
    return {"reservation": row2dict(reservation)}, 200

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
    rental: Rental = RENTAL_DB.getActiveRentalOfTheUser(current_user.get_id())
    if rental is None:
        return BAD_REQUEST
    pending: PendingRental = rental_timer_task.getRental(rental.rentalId)
    if pending is not None:
        r = row2dict(rental)
        r["mileage"] = pending.distance
        r["cost"] = gr_to_pln_gr(pending.calculate_current_cost())
        return {"rental": r}
    return {"rental": rental}, 200


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
        d = row2dict(rental.rent)
        d["mileage"] = rental.distance
        d["cost"] = gr_to_pln_gr(rental.calculate_current_cost())
        return {"rental": d}, 200
    r = RENTAL_DB.getRental(current_user.get_id(), rentalId=rent_id)
    if r is None:
        return BAD_REQUEST
    return {"rental": row2dict(r)}, 200


@app.route("/rent/rent/<rent_id>", methods=["DELETE"])
@login_required
def finishRent(rent_id):
    if not rental_timer_task.endRent(rent_id):
        return BAD_REQUEST
    return EMPTY_OK
