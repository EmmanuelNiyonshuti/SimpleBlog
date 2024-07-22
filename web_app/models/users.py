from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app, url_for, request, redirect
from web_app import db, login_manager, bcrypt
from flask_login import current_user
from flask_login import UserMixin

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


    def set_pwd(self, password):
        """
        hash password
        """
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_pwd(self, password):
        """
        Verify the password
        """
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "is_verified": self.is_verified,
        }


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

