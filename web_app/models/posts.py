"""
This module comprises Post model.
"""
from datetime import datetime
from web_app import db


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



    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "date_posted": self.date_posted.isoformat(),
            "content": self.content,
            "user_id": self.user_id,
        }


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"