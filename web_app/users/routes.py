"""
This module defines routes for user-related functionalities, including registration,
login, account management, and password reset.
"""
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint, session
from web_app import db, bcrypt
from web_app.users.forms import (RegistrationForm, LoginForm, UpdateForm,
RequestResetForm, ResetPasswordForm)
import email_validator
from web_app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from web_app.users.utils import (save_picture, send_reset_email,
                                send_confirmation_email, verify_email_token)

users = Blueprint("users", __name__)

@users.route("/register", methods=['POST', 'GET'])
def register():
    """
    Handle user registration.

    If the user is already authenticated, redirects to the home page.
    On successful form submission, hashes the password, stores user data in a dictionary,
    sends a confirmation email, flashes a success message, and redirects to the thank you page.

    Returns:
        Redirects to home page if authenticated, otherwise renders the registration page.
    """
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
        send_confirmation_email(user_data)
        flash("a confirmation link has been sent to your email address", "success")
        return redirect(url_for("users.thank_you"))
    return render_template('register.html', title="Register", form=form)


@users.route("/thank_you", methods=['POST', 'GET'])
def thank_you():
    """
    Display a thank you page after user registration.

    Returns:
        Renders the thank you page.
    """
    return render_template("blank.html")

@users.route("/confirm_email/<token>", methods=['POST', 'GET'])
def confirm_email(token):
    """
    Handle email confirmation.

    Validates the token, retrieves user data from it, and creates a new user in the database.
    Flashes appropriate messages based on the token validation result.

    Args:
        token (str): The token sent to the user's email for confirmation.

    Returns:
        Redirects to login page if successful, otherwise to the registration page.
    """
    data = verify_email_token(token)
    if not data:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.register"))
    new_user = User(username=data["username"],
                    email=data["email"],
                    password=data["password"],
                    is_verified=True)
    db.session.add(new_user)
    db.session.commit()
    session.pop("user_data", None)
    flash('Your account has been verified, you can now login', 'success')
    return redirect(url_for("users.login"))

@users.route("/login", methods=["GET", "POST"])
def login():
    """
    Handle user login.

    If the user is already authenticated, redirects to the home page.
    On successful form submission, checks user credentials and logs in the user.

    Returns:
        Redirects to home page if authenticated, otherwise renders the login page.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.is_verified and user.verify_pwd(form.password.data):
                login_user(user, form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login Unseccessful. Please check email and password", "danger")
    return render_template("login.html", title="login", form=form)


@users.route("/logout")
def logout():
    """
    Handle user logout.

    Logs out the current user and redirects to the home page.

    Returns:
        Redirects to the home page.
    """
    logout_user()
    return redirect(url_for("main.home"))

@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    """
    Handle account update.

    Displays and updates the user's account information, including username, email, and profile picture.

    Returns:
        Renders the account page with the update form.
    """
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
    """
    Handle account deletion.

    Deletes the current user's account from the database.

    Returns:
        Redirects to the home page.
    """
    user_id = current_user.id
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("You have successfully deleted your Account", "success")
    return redirect(url_for("main.home"))

@users.route("/user/<string:username>")
def user_posts(username):
    """
    Display posts by a specific user.

    Args:
        username (str): The username of the user whose posts are to be displayed.

    Returns:
        Renders the user posts page with the user's posts.
    """
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
    .order_by(Post.date_posted.desc())\
    .paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    """
    Handle password reset request.

    If the user is authenticated, redirects to the home page.
    On successful form submission, sends a password reset email.

    Returns:
        Redirects to the thank you page if authenticated, otherwise renders the reset request page.
    """
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
    """
    Handle password reset token verification.

    If the user is authenticated, redirects to the home page.
    On successful token verification, allows the user to reset the password.

    Args:
        token (str): The token sent to the user's email for password reset.

    Returns:
        Redirects to home page if authenticated, otherwise renders the reset token page.
    """
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
