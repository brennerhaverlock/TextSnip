# Create your forms here.

from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField, DecimalField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from text_snip.models import Post, PostCategory, User
from text_snip import db
from text_snip import bcrypt


class PostForm(FlaskForm):

    title = StringField('Post Title', validators=[DataRequired(), Length(min=3, max=80)])
    description = StringField('Description', validators=[DataRequired(), Length(min=3, max=400)])
    post_id = db.Column(
        db.Integer, db.ForeignKey('post.id'), nullable=False)
    submit = SubmitField('Submit')

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password',
     validators=[DataRequired(), Length(min=3, max=80)])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')