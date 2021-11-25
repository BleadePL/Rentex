from flask import request, Response, Request
from flask_login import login_user, logout_user, login_required, current_user

from backend.db_interface import DatabaseInterface
from database_access import RENTAL_DB
from flask_main import app, login, EMPTY_OK, BAD_REQUEST


@app.route("/service", methods=["POST"])
@login_required
def startService():
    pass


@app.route("/service/<service_id>", methods=["GET"])
@login_required
def getService(service_id: str):
    pass


@app.route("/service/<service_id>", methods=["DELETE"])
@login_required
def deleteService(service_id: str):
    pass


@app.route("/service/car/<car_id>", methods=["GET"])
@login_required
def getServices(car_id: str):
    pass
