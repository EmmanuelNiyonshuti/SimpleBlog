"""
This script initializes and runs the Flask application.

It sets up the application context and starts the server.
"""
from web_app import create_app, db
from web_app.models import User, Post

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        app.run(host="0.0.0.0")
