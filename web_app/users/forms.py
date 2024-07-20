"""
This module contains form classes for user interactions with the application.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from web_app.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
                                    DataRequired(),
                                    Length(min=2, max=20, message="please provide a valid username"),
                                    Regexp("^[A-Za-z][A-Za-z0-9_]*$", 0,
                                    "username must comprise letters, numbers, dots or underscores")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is taken. Please choose a different username!")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email is taken. Please choose a different email!")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateForm(FlaskForm):
    username = StringField('Username', validators=[
                                    DataRequired(),
                                    Length(min=2, max=20, message="please provide a valid username"),
                                    Regexp("^[A-Za-z][A-Za-z0-9_]*$", 0,
                                    "username must comprise letters, numbers, dots or underscores")])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])

    submit = SubmitField('Update')

class RequestResetForm(FlaskForm):
    email = StringField("email",
                        validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            return ValidationError("There is no account with that email. You must register first.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Cofirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")