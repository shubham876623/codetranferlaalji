import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import jsonify
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from flask_sqlalchemy import sqlalchemy
import shutil

from application import app, db, bcrypt
from application.forms import RegisterForm, LoginForm
from application.models import User
from application.schema import UserSchema
from sqlalchemy import extract
from application.database import db

import os


user_schema = UserSchema()
users_schema = UserSchema(many=True)


def get_part_of_day(hour):
    return (
        "morning" if 5 <= hour <= 11
        else
        "afternoon" if 12 <= hour <= 17
        else
        "evening"
    )


time = int(datetime.now().strftime("%H"))


@app.route("/", methods=["GET", 'POST'])
@login_required
def home():
    cursor = db.get_cursor()
    cursor.execute("select * from j2c_court_transaction_log ORDER BY ID DESC")
    trans_logs = cursor.fetchall()[:20]
    logging_list = []
    for tran_log in trans_logs:
        log_dict = {}
        tran_log = list(tran_log)
        log_dict.update({'id':tran_log[0],'jus_uuid': str(tran_log[2]),'courtno':tran_log[3],'action':tran_log[4],'caseid':tran_log[5],'tran_type':tran_log[7],'operation':tran_log[8],'dto_sent':tran_log[10],'resp_dto':tran_log[11],'resp_code':tran_log[12],'timestamp':tran_log[14]})
        logging_list.append(log_dict)
    return render_template("dashboard.html",logging_list=logging_list)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/login", methods=["POST", "GET"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    # loading the form
    login_ = LoginForm()
    # # checking the form data status
    if login_.validate_on_submit():
        user = User.query.filter_by(email=login_.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login_.password.data):
            next_page = request.args.get("next")
            login_user(user)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login unsuccessful Please Check Email and Password", "danger")
    return render_template("login.html", form=login_)


@app.route("/register", methods=["GET", "POST"])
# @login_required
def register():
    # checking if the current user is logged
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    register = RegisterForm()
    if register.validate_on_submit():
        # hashing the password
        hashed_password = bcrypt.generate_password_hash(register.password.data).decode("utf-8")
        # adding the password to the database
        try:
            user = User(firstname=register.firstname.data, surname = register.surname.data,phonenumber=register.phonenumber.data,email=register.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f"Account Created successfully", "success")
        except sqlalchemy.exc.IntegrityError:
            flash("User By That Username Exists", "warning")
        return redirect(url_for('login'))
    return render_template("register.html", form=register)





