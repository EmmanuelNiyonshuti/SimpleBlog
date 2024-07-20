"""
This module provides utility functions for handling images and sending emails.
"""
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from web_app import mail
from itsdangerous import URLSafeTimedSerializer as Serializer

def save_picture(form_picture):
    """
    Save the user's profile picture.

    Generates a random hex to use as the filename, resizes the image to 125x125 pixels,
    and saves it to the 'static/profile_pics' directory.

    Args:
        form_picture: The uploaded picture file.

    Returns:
        str: The filename of the saved picture.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_fn)

    outpust_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(outpust_size)

    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    """
    Send a password reset email to the user.

    Generates a reset token and sends an email with the reset link.

    Args:
        user: The user requesting the password reset.
    """
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                    sender="noreply@demo.com",
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no change will be made.
'''
    mail.send(msg)



def generate_confirmation_token(username, email, password):
    """
    Generate an email confirmation token.

    Creates a token containing the user's username, email, and password.

    Args:
        username: The user's username.
        email: The user's email.
        password: The user's hashed password.

    Returns:
        str: The generated token.
    """
    s = Serializer(current_app.config["SECRET_KEY"])
    return s.dumps({"username": username, "email": email, "password": password}, salt=current_app.config['SECURITY_PASSWORD_SALT'])

def verify_email_token(token, max_age=1800):
    """
    Verify an email confirmation token.

    Decodes the token and checks its validity.

    Args:
        token: The token to verify.
        max_age: The maximum age of the token in seconds.

    Returns:
        dict: The decoded data if the token is valid, otherwise None.
    """
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        data = s.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=max_age)
    except:
        return None
    return data


def send_confirmation_email(user_data):
    """
    Send an email confirmation email to the user.

    Generates a confirmation token and sends an email with the confirmation link.

    Args:
        user_data: A dictionary containing the user's data (username, email, password).
    """
    token = generate_confirmation_token(user_data["username"], user_data["email"], user_data["password"])
    msg = Message("Email verification link",
                    recipients=[user_data["email"]])
    msg.body = f'''To confirm your email, visit the following link:
{url_for('users.confirm_email', token=token, _external=True)}
If you did not make this request then simply ignore this email and no change will be made. Please do not reply to this email
'''
    mail.send(msg)
