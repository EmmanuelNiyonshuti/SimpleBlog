from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session
from web_app import db, bcrypt
from web_app.users.forms import (RegistrationForm, LoginForm, UpdateForm,
RequestResetForm, ResetPasswordForm)
import email_validator
from web_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from web_app.users.utils import save_picture, send_reset_email, send_confirmation_email, verify_email_token 

users = Blueprint("users", __name__)

@users.route("/register", methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_data ={
            "username": form.username.data,
            "email": form.email.data,
            "password": hashed_pwd
        }
        session["user_data"] = user_data
        send_confirmation_email(user_data)
        flash("a confirmation link has been sent to your email address", "success")
        return redirect(url_for("users.thank_you"))
    return render_template('register.html', title="Register", form=form)


@users.route("/thank_you", methods=['POST', 'GET'])
def thank_you():
    return render_template("blank.html")

@users.route("/confirm_email/<token>", methods=['POST', 'GET'])
def confirm_email(token):
    email = verify_email_token(token)
    if not email:
        flash("That is an invalid or expired token", "warning")
    user = session.get("user_data")
    if user and user["email"] == email:
        new_user = User(username=user["username"],
                        email=user["email"],
                        password=user["password"],
                        is_verified=True)
        db.session.add(new_user)
        db.session.commit()
        session.pop("user_data", None)
        flash('Your account has been verified, you can now login', 'success')
        return redirect(url_for("users.login"))
    else:
        return redirect(url_for("users.register"))

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_verified and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unseccessful. Please check email and password", "danger")
    return render_template("login.html", title="login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                current_user.image_file = picture_file
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Your account has been updated!", "success")
            return redirect(url_for("main.home"))
    elif request.method == "GET":
        form.username.data= current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template("account.html", title="account",
                                                image_file=image_file, form=form)

@users.route("/account/delete", methods=["GET", "POST"])
@login_required
def account_delete():
    user_id = current_user.id
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("You have successfully deleted your Account", "success")
    return redirect(url_for("main.home"))

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
    .order_by(Post.date_posted.desc())\
    .paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("users.thank_you"))
    return render_template("reset_request.html", title="Reset Password", form=form)

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pwd
        db.session.commit()
        flash(f'Your Account has been updated! You are now able to login!', 'success')
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
