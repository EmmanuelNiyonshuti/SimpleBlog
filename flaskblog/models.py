from datetime import datetime
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app, url_for, request, redirect
from flaskblog import db, login_manager
from flask_login import current_user
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView
# from flask_admin import AdminIndexView, expose

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # user_role = db.Column(db.String(30), nullable=False, default="user")
    posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")


class AdminModelView(ModelView):
    def is_accessible(self):
        """
        determines if the current user can access the admin view.
        returns True if the user is authenticated.
        """
        return current_user.is_authenticated and current_user.username == "emmanuel"

    def inaccessible_callback(self, name, **kwargs):
        """
        redirects user to the login page if it is not authenticated.
        """
        return redirect(url_for("users.login", next=request.url))

# class MyAdminIndexView(AdminIndexView):
#     @expose("/")
#     def index():
#         return self.render("admin/index.html")

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"])
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token, expires_sec)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
