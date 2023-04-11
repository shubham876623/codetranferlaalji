import random
import re
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from flask_login import current_user

from kleenbin import db
from kleenbin.models import User, Recovery, UserSession, Customer
from kleenbin.schema import UserSchema, RecoverySchema, CustomerSchema
from flask import redirect, url_for, flash
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from kleenbin import client

# mpesa
user_schema = UserSchema()
users_schema = UserSchema(many=True)

recovery_schema = RecoverySchema()
recoveries_schema = RecoverySchema(many=True)

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


def get_customers_by_provice(provice):
    ref = Customer.query.all()
    return customers_schema.dump(ref)


def password_code_request(to, subject):
    if re.fullmatch("[^@]+@[^@]+\.[^@]+", to):
        user_info = User.query.filter_by(email=to).first()
        final = True
        if user_info:
            user = user_info
            info = save_code(user.id)
            data = {
                "to": to,
                "subject": subject,
                "code": info["code"]
            }
            res = requests.post(
                "http://159.65.144.235:3000/send/email/code", json=data)
            final = True
        else:
            final = False
    else:
        final = False
    return {"msg": final}


def save_code(user):
    code = random_four()
    delete_old_codes(user)
    lookup = Recovery(user, code)
    db.session.add(lookup)
    db.session.commit()
    code = recovery_schema.dump(lookup)
    return code


def delete_old_codes(user_id):
    codes = Recovery.query.filter_by(user=user_id).all()
    for code in codes:
        db.session.delete(code)
        db.session.commit()
    return dict()


def code_exists(email, code):
    user_ = User.query.filter_by(email=email).first()
    code = Recovery.query.filter_by(code=code).filter_by(
        user=user_.id).first() if user_ else False
    return True if code else False


def random_four():
    rand = random.getrandbits(30)
    numbers = str(rand)
    final = [numbers[i:i + 4] for i in range(0, len(numbers), 4)]
    final = f"{final[0]}-{final[1]}"
    return final


def email(_to, subject, body):
    _from = "admin@kleenbin.com"
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = _from
    message["To"] = _to
    # Turn these into plain/html MIMEText objects
    part = MIMEText(body, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    message.attach(part)
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.kleenbin.com", 465, context=context) as server:
        server.login(_from, "Japanitoes")
        if server.sendmail(_from, _to, message.as_string()):
            return True
        else:
            return False


def user_has_branch_check(f):
    def with_connection_(args, *kwargs):
        session = UserSession.query.filter_by(user=current_user.id).first()
        db.session.commit()
        if session:
            print("user ... ")
        else:
            print("no user ... ")
        return session

    return with_connection_


def user_session(user):
    session = UserSession.query.filter_by(user=user.id).first()
    if not session:
        flash("Error! Please select location first", "danger")
        return redirect(url_for("home"))


def send_message(to, message):
    valid = carrier._is_mobile(number_type(phonenumbers.parse(to)))
    if valid:
        message = client.messages \
            .create(body=message, from_='+17163259349', to=to)
        final = message.sid
        print("phone number valid")
    else:
        final = False
        print("phone NOT number valid")
    return final
