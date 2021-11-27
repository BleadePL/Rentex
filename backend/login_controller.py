import os
import random
import secrets
import time

from flask import request, Response, Request
from flask_login import login_user, logout_user, login_required, current_user

from backend.db_interface import DatabaseInterface
from backend.utils import parse_required_fields
from database_access import RENTAL_DB
from flask_main import app, login, EMPTY_OK, BAD_REQUEST, LoggedInUser

RENTAL_DB: DatabaseInterface

logged_in_users: list[LoggedInUser]


@login.unauthorized_handler
def unauthorised():
    return Response(status=401, response={})


@login.request_loader
def load_user_from_request(request: Request):
    session_id = request.headers.get("Session-Token")
    if session_id:
        for e in logged_in_users:
            if e.session_token == session_id:
                return e
    return None


@app.route("/login/login", methods=["POST"])
def loginToSystem():
    if request.json is None:
        return BAD_REQUEST
    parsed = parse_required_fields(request.json, ["login", "password"])
    if parsed is None:
        return BAD_REQUEST
    l = parsed["login"]
    pas: str = parsed["password"]
    # TODOREMOVE
    if l == "test" and pas == "test":
        user_id = "test123"
    else:
        user_id = RENTAL_DB.authUser(l, pas.encode("utf-8"))
    if user_id is not None:
        u = next((user for user in logged_in_users if user.get_id() == user_id), None)
        if u is not None:
            logged_in_users.remove(u)
        token = secrets.token_hex()
        user = LoggedInUser(user_id, token)
        login_user(user)
        logged_in_users.append(user)
        return {'token': token}
    else:
        return {}, 401


@app.route("/login/logout", methods=["POST"])
@login_required
def logout():
    global logged_in_users
    logged_in_users.remove(current_user)
    logout_user()
    return EMPTY_OK


@app.route("/login/sendtoken", methods=["POST"])
@login_required
def sendToken():
    if current_user.activation_token_time is None or (time.time() - current_user.activation_token_time) > 120:
        RENTAL_DB.setActivationToken(userId=current_user.get_id(), token=str(random.randint(100000, 999999)))
        current_user.activation_token_time = time.time()
        return EMPTY_OK
    else:
        return BAD_REQUEST


@app.route("/login/status", methods=["GET"])
@login_required
def getStatus():
    s = RENTAL_DB.getAccountStatus(userId=current_user.get_id())
    if s is None:
        return Response(status=500)
    else:
        return Response(response={"status": s})


@app.route("/login/register", methods=["POST"])
def register():
    if request.json is None:
        return {'error': "UNKNOWN"}, 400

    register_request = parse_required_fields(request.json,
                                             ["name", "surname", "gender", "login", "password", "address", "email",
                                              "pesel"])
    if RENTAL_DB.isUserWithEmailInDB(register_request["email"]):
        return {'error': "EMAIL_USED"}, 400
    elif RENTAL_DB.isUserWithLoginInDB(register_request["login"]):
        return {"error": "LOGIN_USED"}, 400

    # TODO: Validation of other data
    user_id = RENTAL_DB.registerUser(name=register_request["name"], surname=register_request["surname"],
                                     gender=register_request["gender"], login=register_request["login"],
                                     password=register_request["passwprd"], address=register_request["address"],
                                     email=register_request["email"], pesel=register_request["pesel"])
    if user_id is None:
        return {"error": "UNKNOWN"}, 400
    return {"userId": user_id}, 200


@app.route("/login/activate", methods=["GET"])
def activate():
    token = request.args["token"]
    if RENTAL_DB.activateAccount(token):
        return EMPTY_OK
    return BAD_REQUEST


@app.route("/login/uploadphoto", methods=["POST"])
@login_required
def uploadPhoto():
    if request.files is None:
        return 400
    if "front" not in request.files and "back" not in request.files:
        return 400
    front = request.files["front"]
    front.save(PHOTOS_TARGET + "/" + current_user.get_id() + "_front_" + front.filename)
    back = request.files["back"]
    back.save(PHOTOS_TARGET + "/" + current_user.get_id() + "_back_" + back.filename)
    return {}, 200


print("Login_controller" + __name__)

if __name__ == "login_controller":
    logged_in_users = [LoggedInUser("test123", "testTokenAdmin")]
    PHOTOS_TARGET = "licences"
    if not os.path.exists(PHOTOS_TARGET):
        os.mkdir(PHOTOS_TARGET)
