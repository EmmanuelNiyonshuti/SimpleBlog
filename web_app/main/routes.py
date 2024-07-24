"""
main.py
-------

This module defines the main routes for the Flask blogging application, including the home and about pages.
"""

from flask import render_template, request, Blueprint
from web_app.models import Post

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    """
    Display the home page with a list of blog posts.

    The posts are paginated, showing 5 posts per page. The page number is 
    retrieved from the request arguments.

    Returns:
        Response: Rendered home page with blog posts.
    """
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)

@main.route("/about")
def about():
    """
    Display the about page.

    Returns:
        Response: Rendered about page with a title.
    """
    return render_template("about.html", title='about')