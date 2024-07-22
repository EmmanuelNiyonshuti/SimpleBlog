"""
This module initializes and configures the Flask application and its extensions.

The `create_app` function is responsible for setting up the application with the necessary
configurations and registering the blueprints for different parts of the application. 

Extensions initialized in this module:
- SQLAlchemy for database management
- Flask-Migrate for handling database migrations
- Bcrypt for password hashing
- Flask-Login for user session management
- Flask-Mail for sending emails
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from web_app.config import Config
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
jwt = JWTManager() 

mail = Mail()
migrate = Migrate()
cors = CORS()
def create_app(config_class=Config):
    """
    Create and configure the Flask application.

    Args:
        config_class (class, optional): The configuration class to use. Defaults to Config.

    Returns:
        Flask app: The configured Flask application instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    """Initialize extensions with the app"""
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/*": {"origins": "0.0.0.0"}})

    from web_app.users.routes import users
    from web_app.posts.routes import posts
    from web_app.main.routes import main
    from web_app.errors.handlers import errors
    from api.v1.views import app_views
    """Register blueprints"""
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(app_views)

    return app
