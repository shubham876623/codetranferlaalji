import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from flask import jsonify
from flask import flash, redirect, request, send_file
from flask_login import login_user, logout_user, login_required, current_user
from kleenbin.utility import email as send_email, send_message
from kleenbin import app, db, bcrypt
from kleenbin.models import  MessageTransaction


def saveTransaction(time, subject, message, media):
    transaction_obj = MessageTransaction(time, subject, message, media)
    db.session.add(transaction_obj)
    db.session.commit()

@app.route("/send-email-or-mess", methods=["POST", "GET"])
@login_required
def send_message_and_email():
    if request.method=='POST':
        transaction_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        activity = request.json.get('activity') 
        if activity == 'send_mail':
            to = request.json.get('email')
            subject = request.json.get('subject')
            email_body = request.json.get('email_body')
            print(to, subject, email_body)
            is_send = send_email(to, subject, email_body)
            if is_send:
                saveTransaction(transaction_time, subject, email_body, 'Mail')
                flash('Email sent Successfully!','success')
                return jsonify({'message':'Email sent Successfully!'})
            else:
                flash('Error in sending Email!','danger')
                return jsonify({'message':'Error in sending Email!'})
        else:
            to = request.json.get('contact')
            message = request.json.get('message')
            is_send = send_message(to, message)
            saveTransaction(transaction_time, message, message, 'SMS')
            if is_send:
                flash('Message sent Successfully!','success')
                return jsonify({'message':'Message sent Successfully!'})
            else:
                flash('Error in sending Message!','danger')
                return jsonify({'message':'Error in sending Message!'})
    else:
        flash(f"Error in Sending!", "danger")