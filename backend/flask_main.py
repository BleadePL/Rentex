import secrets

from flask import Flask
from flask_login import LoginManager

app = Flask("Wypozyczalnia Aut BACKEND")
app.secret_key = secrets.token_hex()
login = LoginManager(app)
# auth = Authorize()
print("Initialized!")

import controllers.login_controller
