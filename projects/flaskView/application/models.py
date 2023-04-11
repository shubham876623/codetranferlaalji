from datetime import datetime
from flask_login import UserMixin
import secrets
from application import db, ma, login_manager
from dateutil import parser
import random
from flask import request, redirect, url_for
from sqlalchemy.sql import func
from application.jsontype_models import JsonEncodedDict


def ticket_unique() -> int:
    return secrets.token_hex(16)


def week_number():
    return datetime.now().strftime("%V")


def final_schedule_number():
    return f"{ticket_unique()}.{week_number()}"


def default_preq_date():
    return parser.parse("01/01/1970")


@login_manager.user_loader
def load_user(user_id):                            
    try:
        return User.query.get(int(user_id))
    except Exception:
        return redirect(url_for(request.url_rule.endpoint))


def verify_token():
    return int(str(random.getrandbits(32))[:6])


def midnight():
    return parser.parse("00:00")


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(12), nullable=False)
    surname = db.Column(db.String(12), nullable=False)
    phonenumber = db.Column(db.String(12), unique=True, nullable=False)
    email = db.Column(db.String(48), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, firstname, surname, phonenumber, email, password):
        self.firstname = firstname
        self.surname = surname
        self.phonenumber = phonenumber
        self.email = email
        self.password = password
