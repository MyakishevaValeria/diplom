from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = '1234v'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rzd.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SESSION_COOKIE_NAME"] = "myCOOKIE_MONster528"
db = SQLAlchemy(app)
manager = LoginManager(app)

from sweater import models, routes

db.create_all()