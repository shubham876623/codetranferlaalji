from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange

from application.models import User


class RegisterForm(FlaskForm):
    firstname = StringField("Firstname", validators=[DataRequired()])
    surname = StringField("Surname", validators=[DataRequired()])
    phonenumber = StringField("Phone Number", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_password', message='Passwords '
                                                                                                         'must '
                                                                                                         'match')])
    confirm_password = PasswordField("Confirm Password")
    submit = SubmitField("Add User")

    # validation from checking the email
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Email Already Taken. Please Choose Another One")


class LoginForm(FlaskForm):
    email = StringField("Email or Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

