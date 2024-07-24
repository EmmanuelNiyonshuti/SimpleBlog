"""
This module comprises Comment model.
"""
from datetime import datetime
from web_app import db

class Comment(db.Model):
    """
    Comment model representing a comment on a blog post.

    Attributes:
        id (int): Primary key.
        content (str): Content of the comment.
        date_commented (datetime): Date and time when the comment was created.
        user_id (int): Foreign key to the User model.
        author (relationship): Relationship to the User model.
        post_id (int): Foreign key to the Post model.
        post (relationship): Relationship to the Post model.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)    
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)


    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "date_commented": self.date_commented,
            "user_id": self.user_id,
            "post_id": self.post_id,
        }

    def __repr__(self):
        return f"Comment('{self.author}', '{self.content}', '{self.post}')"