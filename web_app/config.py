import os
from dotenv import load_dotenv
load_dotenv()

db_user = os.getenv("BLOG_MYSQL_USER")
db_pwd = os.getenv("BLOG_MYSQL_PWD")
db_host = os.getenv("BLOG_MYSQL_HOST")
db_name = os.getenv("BLOG_MYSQL_DB")



class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{db_user}:{db_pwd}@{db_host}/{db_name}"
    # SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_pwd}@{db_host}/{db_name}"

    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("EMAIL_USER")
    MAIL_PASSWORD = os.getenv("EMAIL_PWD")
    FLASK_ADMIN_SWATCH = "sandstone"