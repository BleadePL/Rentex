import secrets
from flask import Flask
from flask_login import LoginManager

app: Flask
login: LoginManager

print(__name__)


def initialize():
    global app, login, auth
