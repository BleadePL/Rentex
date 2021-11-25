from flask import request, Response, Request
from flask_login import login_user, logout_user, login_required, current_user

from backend.db_interface import DatabaseInterface
from database_access import RENTAL_DB
from flask_main import app, login, EMPTY_OK, BAD_REQUEST


@app.route("/rent/reservation/<reservation_id>", methods=["GET"])
@login_required
def gerReservation(reservation_id: str):
    pass


@app.route("/rent/reservation/<reservation_id>", methods=["DELETE"])
@login_required
def deleteReservation(reservation_id: str):
    pass


@app.route("/rent/reservate", methods=["POST"])
@login_required
def reservate():
    pass


@app.route("/rent/rent", methods=["POST"])
@login_required
def rent():
    pass


@app.route("/rent/rent/<rent_id>", methods=["GET"])
@login_required
def getRent(rent_id):
    pass


@app.route("/rent/rent/<rent_id>", methods=["DELETE"])
@login_required
def finishRent(rent_id):
    pass
