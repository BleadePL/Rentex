import secrets

from flask import Flask, Response
from flask_login import LoginManager

app = Flask("Wypozyczalnia Aut BACKEND")
app.secret_key = secrets.token_hex()
login = LoginManager(app)
BAD_REQUEST = {}, 400
EMPTY_OK = {}, 200
# auth = Authorize()
print("Initialized!")

import login_controller
import user_controller
import service_controller
import browse_controller
