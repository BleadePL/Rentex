import secrets

from database_access import RENTAL_DB
from flask_main import app, login
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from flask import request, Response, Request, Flask

from backend.db_interface import DatabaseInterface

app: Flask
login: LoginManager
RENTAL_DB: DatabaseInterface
bad_request = Response(status=400, response={})


class LoggedInUser:
    def __init__(self, user_id, session_token):
        self.id = user_id
        self.session_token = session_token

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


logged_in_users: list[LoggedInUser] = []


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
def login():
    token = secrets.token_hex()
    if request.json == None:
        return
    user = LoggedInUser("09213u8jabsd", token)
    login_user(user)
    global logged_in_users
    logged_in_users.append(user)
    return {'token': token}


@app.route("/login/logout", methods=["POST"])
@login_required
def logout():
    u = current_user
    print(u)
    logged_in_users.remove(u)
    logout_user()
    return "Success"
