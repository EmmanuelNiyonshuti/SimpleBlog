import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from web_app import mail
from itsdangerous import URLSafeTimedSerializer as Serializer

def save_picture(form_picture):
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
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                    sender="noreply@demo.com",
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no change will be made.
'''
    mail.send(msg)



def generate_confirmation_token(email):
    s = Serializer(current_app.config["SECRET_KEY"])
    return s.dumps(email)

def verify_email_token(token, max_age=1800):
    s = Serializer(current_app.config["SECRET_KEY"])
    try:
        email = s.loads(token, max_age=max_age)
    except:
        return None
    return email


def send_confirmation_email(user_data):
    token = generate_confirmation_token(user_data["email"])
    msg = Message("Email verification link",
                    recipients=[user_data["email"]])
    msg.body = f'''To confirm you email, visit the following link:
{url_for('users.confirm_email', token=token, _external=True)}
If you did not make this request then simply ignore this email and no change will be made. Please do not reply to this email
'''
    mail.send(msg)
