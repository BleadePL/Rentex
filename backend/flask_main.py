from flask import Flask, request, session, abort, Response, Request
from flask_authorize import Authorize
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

import secrets

app = Flask("Wypozyczalnia Aut BACKEND")
app.secret_key = secrets.token_hex()
login = LoginManager(app)
auth = Authorize()


class LoggedInUser:
    def __init__(self, id, session_token):
        self.id = id
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


# @login.user_loader
def load_user(user_id):
    for t in logged_in_users:
        tok, user = t

    return {"userId": user_id}


@login.request_loader
def load_user_from_request(request: Request):
    session_id = request.headers.get("Session-Token")
    if session_id:
        for e in logged_in_users:
            if e.session_token == session_id:
                return e
    return None


@app.route("/")
@login_required
def test():
    print(current_user)
    return {'status': "Logged in"}


@app.route("/login/login", methods=["POST"])
def login():
    print(request.json)
    print(request.json["login"])
    token = secrets.token_hex()
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
