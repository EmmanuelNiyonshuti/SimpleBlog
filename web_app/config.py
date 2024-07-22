"""
This module contains configuration settings for the Flask application.

It includes database configuration, email settings, and secret keys.

Configuration Parameters:
- SECRET_KEY: Key used for session encryption and security
- SQLALCHEMY_DATABASE_URI: URI for the PostgreSQL database connection
- MAIL_SERVER: SMTP server for sending emails
- MAIL_PORT: Port for the SMTP server
- MAIL_USE_TLS: Enable TLS for email communication
- MAIL_USERNAME: Email username for authentication
- MAIL_PASSWORD: Email password for authentication
- MAIL_DEFAULT_SENDER: Default sender for outgoing emails
- FLASK_ADMIN_SWATCH: Admin theme for Flask-Admin
- SECURITY_PASSWORD_SALT: Salt for password hashing
"""

import os
from dotenv import load_dotenv
load_dotenv()

"""
local dvpt db configs
db_user = os.getenv("BLOG_MYSQL_USER")
db_pwd = os.getenv("BLOG_MYSQL_PWD")
db_host = os.getenv("BLOG_MYSQL_HOST")
db_name = os.getenv("BLOG_MYSQL_DB")
"""

db_user = os.getenv("BLOG_POSTGRESQL_USER")
db_pwd = os.getenv("BLOG_POSTGRESQL_PWD")
db_host = os.getenv("BLOG_POSTGRESQL_HOST")
db_name = os.getenv("BLOG_POSTGRESQL_DB")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    """SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pwd}@{db_host}/{db_name}" """
    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pwd}@{db_host}/{db_name}"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL_USER")
    MAIL_PASSWORD = os.getenv("EMAIL_PWD")
    MAIL_DEFAULT_SENDER = ('simpleblog', 'no-reply@simpleblog.com')
    FLASK_ADMIN_SWATCH = "sandstone"
    SECURITY_PASSWORD_SALT=os.getenv("SECURITY_PASSWORD_SALT")
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
