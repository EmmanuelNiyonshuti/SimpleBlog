"""
Import all database models and define relationships among them

Models:
- User: Represents a user in the application
- Post: Represents a post created by a user
- Comment: Represents a comment on a post
"""

from .users import User
from .posts import Post
from .comments import Comment
from web_app import db


User.posts = db.relationship('Post', backref='author', lazy=True, cascade="all, delete-orphan")
User.comments = db.relationship("Comment", back_populates="author", cascade="all, delete-orphan")


Post.comments = db.relationship("Comment", back_populates="post", lazy=True, cascade="all, delete-orphan")



Comment.post = db.relationship("Post", back_populates="comments")
Comment.author = db.relationship("User", back_populates="comments")
