from flask_wtf import Form
from wtforms import StringField, validators, PasswordField, TextAreaField
from wtforms.fields.html5 import EmailField
from blog.models import Category
from wtforms.ext.sqlalchemy.fields import  QuerySelectField
from flask_wtf.file import FileField, FileAllowed

class SetupForm(Form):
    name = StringField('Blog Name', [
            validators.Required(),
            validators.Length(max=80)
        ])
    fullname = StringField('Full Name', [validators.Required()])
    email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
    username = StringField('Username', [
            validators.Required(),
            validators.Length(min=4, max=25)
        ])
    password = PasswordField('New Password', [
            validators.Required(),
            validators.EqualTo('confirm', message='Passwords must match'),
            validators.Length(min=4, max=80)
        ])
    confirm = PasswordField('Repeat Password')

def categories():
    return Category.query
    

class PostForm(Form):
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
        ])
    title = StringField('Title', [
        validators.Required(),
        validators.Length(max=140)
        ])
    body = TextAreaField('Content', validators=[validators.Required()])
    category = QuerySelectField('Category', query_factory=categories, allow_blank=True)
    new_category=StringField('New Category')


class CommentForm(Form):
    comment = StringField('Comment', [
            validators.Required()
        ])
