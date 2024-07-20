"""
This module defines the database models for the application, including User, Post,
and Comment models. It also provides methods for user authentication and managing
relationships between models.

Models:
- User: Represents a user in the application
- Post: Represents a post created by a user
- Comment: Represents a comment on a post
"""

from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app, url_for, request, redirect
from web_app import db, login_manager
from flask_login import current_user
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView

@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login user loader callback.

    Args:
        user_id (int): The ID of the user to load.

    Returns:
        User: The user object if found, otherwise None.
    """
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """
    User model representing a user in the application.

    Attributes:
        id (int): Primary key.
        username (str): Unique username.
        email (str): Unique email address.
        image_file (str): Filename of the user's profile picture.
        password (str): Hashed password.
        is_verified (bool): Indicates if the user's email is verified.
        posts (relationship): a one to many Relationship to the Post model.
        comments (relationship): a one to many Relationship to the Comment model.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)

    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", back_populates="author", cascade="all, delete-orphan")


    def get_reset_token(self):
        """
        Generate a password reset token.

        Args:
            expires_sec (int, optional): The expiration time of the token in seconds. Defaults to 1800.

        Returns:
            str: The generated token.
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """
        Verify a password reset token.

        Args:
            token (str): The token to verify.
            expires_sec (int, optional): The expiration time of the token in seconds. Defaults to 1800.

        Returns:
            User: The user associated with the token if valid, otherwise None.
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, expires_sec)["user_id"]
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    """
    Post model representing a blog post in the application.

    Attributes:
        id (int): Primary key.
        title (str): Title of the post.
        date_posted (datetime): Date and time when the post was created.
        content (str): Content of the post.
        user_id (int): Foreign key to the User model.
        comments (relationship): a one to many Relationship to the Comment model.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship("Comment", back_populates="post", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class Comment(db.Model):
    """
    Comment model representing a comment on a blog post.

    Attributes:
        id (int): Primary key.
        content (str): Content of the comment.
        date_commented (datetime): Date and time when the comment was created.
        user_id (int): Foreign key to the User model.
        author (relationship): Relationship to the User model.
        post_id (int): Foreign key to the Post model.
        post (relationship): Relationship to the Post model.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    author = db.relationship("User", back_populates="comments")
    
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    post = db.relationship("Post", back_populates="comments")

    def __repr__(self):
        return f"Comment('{self.author}', '{self.content}', '{self.post}')"
