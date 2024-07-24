"""
errors.py
---------

This module defines error handlers for common HTTP error codes in the Flask application.
"""

from flask import Blueprint, render_template

#blueprint for error handling
errors = Blueprint("errors", __name__)

@errors.app_errorhandler(404)
def error_404(error):
    """
    Handle 404 Not Found error.

    Returns:
        Response: Rendered 404 error page with a 404 status code.
    """
    return render_template("errors/404.html"), 404

@errors.app_errorhandler(403)
def error_403(error):
    """
    Handle 403 Forbidden error.

    Returns:
        Response: Rendered 403 error page with a 403 status code.
    """
    return render_template("errors/403.html"), 403

@errors.app_errorhandler(500)
def error_500(error):
    """
    Handle 500 Internal Server Error.

    Returns:
        Response: Rendered 500 error page with a 500 status code.
    """
    return render_template("errors/500.html"), 500