import bcrypt
from flask import request
from flask_login import login_required, current_user

from backend.classes import CreditCard
from db_interface import DatabaseInterface
from flask_main import LoggedInUser
from utils import parse_required_fields, validate_card, execute_card_verification, is_latitude_valid, \
    is_longitude_valid, execute_card_charge, gr_to_pln_gr, pln_gr_to_gr
from database_access import RENTAL_DB
from flask_main import app, EMPTY_OK, BAD_REQUEST

RENTAL_DB: DatabaseInterface
current_user: LoggedInUser


@app.route("/user/details", methods=["GET"])
@login_required
def getUserDetails():
    user = RENTAL_DB.getUser(userId=current_user.get_id())
    if user is None:
        print("THIS IS ILLEGAL STATE")
        return BAD_REQUEST

    return {
        "userId": user.clientId,
        "login": user.login,
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "accountType": user.accountType,
        "status": user.status,
        "balance": user.balance
    }


@app.route("/user/changepasswd", methods=["POST"])
@login_required
def changePassword():
    if request.json in None or "newPasswd" not in request.json or "oldPasswd" not in request.json:
        return {"error": "UNKNOWN"}, 400
    user = current_user.retrieve_user_from_db()
    if user is None:
        print("THIS IS ILLEGAL STATE")
        return {}, 500
    if bcrypt.checkpw(request.json["oldPasswd"], user.password):
        if bcrypt.checkpw(request.json["newPasswd"], user.password):
            return {"error": "USED"}, 400
        RENTAL_DB.changePassword(userId=current_user.get_id(), newPwd=user.password)
        return EMPTY_OK
    return {"error": "INVALID"}, 400


@app.route("/user/updatelocation", methods=["POST"])
@login_required
def updateLocation():
    if request.json is None and "locationLat" not in request.json and "locationLong" not in request.json:
        return BAD_REQUEST
    if not is_latitude_valid(request.json["locationLat"]) or not is_longitude_valid(request.json["locationLong"]):
        return BAD_REQUEST
    if not RENTAL_DB.updateLocation(current_user.get_id(), (request.json["locationLat"], request.json["locationLong"])):
        return {}, 500
    return EMPTY_OK


@app.route("/user/history", methods=["GET"])
@login_required
def getRentalHistory():
    pageIndex = int(request.args["startindex"])
    pageLength = min(int(request.args["pageLength"]), 20)
    return {"rentals": list(map(lambda r: r.__dict__, RENTAL_DB.getUserRentalHistory(current_user.get_id(), pageIndex,
                                                                                     pageLength)))}  # TODO: Suspiciously short


@app.route("/user/cards", methods=["GET"])
@login_required
def getCards():
    cards = RENTAL_DB.getCards(current_user.get_id())
    return {"cards": list(map(lambda card: card.creditCardId, cards))}, 200


@app.route("/user/cards", methods=["POST"])
@login_required
def addCard():
    if request.json is None:
        return {"error": "UNKNOWN"}, 400
    parsed = parse_required_fields(request.json, ["cardNumber", "expirationDate", "cardHolder", "cvv"])
    if parsed is None:
        return {"error": "UNKNOWN"}, 400
    if not validate_card(parsed["cardNumber"]):
        return {"error": "AUTH_ERROR"}, 400
    card = CreditCard(cardNumber=parsed["cardNumber"], expirationDate=parsed["expirationDate"],
                      cardHolderName=parsed["cardHolder"])
    if not execute_card_verification(card, parsed["cvv"]):
        return {"error": "BLOCK_ERROR"}, 400

    if RENTAL_DB.addCard(current_user.get_id(), card):
        return {}
    return {"error": "UNKNOWN"}, 400


@app.route("/user/card/<card_id>", methods=["GET"])
@login_required
def getCard(card_id: str):
    card = RENTAL_DB.getCard(current_user.get_id(), card_id)
    if card is None:
        return BAD_REQUEST

    return {
        "lastDigits": str(card.cardNumber)[-4:],
        "expiration": card.expirationDate,
        "holderName": card.cardHolderName
    }


@app.route("/user/card/<card_id>/charge", methods=["POST"])
@login_required
def charge(card_id: str):
    if request.json is None or "amount" not in request.json or "cvv" not in request.json:
        return BAD_REQUEST
    card = RENTAL_DB.getCard(current_user.get_id(), card_id)
    user = RENTAL_DB.getUser(current_user.get_id())
    if card is None or user is None:
        return BAD_REQUEST

    if execute_card_charge(int(request.json["amount"]) * 100, card.cardNumber, card.expirationDate, request.json["cvv"],
                           card.cardHolderName):
        RENTAL_DB.setNewBalance(current_user.get_id(),
                                gr_to_pln_gr(pln_gr_to_gr(user.balance) + int(request.json["amount"]) * 100))
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/user/card/<card_id>", methods=["DELETE"])
@login_required
def deleteCard(card_id: str):
    if RENTAL_DB.deleteCard(current_user.get_id(), card_id):
        return EMPTY_OK
    else:
        return BAD_REQUEST
