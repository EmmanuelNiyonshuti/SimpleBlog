"""
This module contains form classes for post and comment interactions with the application.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")

class AddComment(FlaskForm):
    body = TextAreaField("body", validators=[InputRequired()])
    respond = SubmitField("respond")
    cancel =  SubmitField("cancel")