# Create your models here.
from sqlalchemy_utils import URLType
from text_snip import db
from text_snip.utils import FormEnum
from flask_login import UserMixin


class PostCategory(FormEnum):
    """Categories of Posts."""
    GENERAL = 'General'
    FUN = 'Fun'
    FOOD = 'Food'
    RANDOM = 'Random'
    WORK = 'Work'
    OTHER = 'Other'

class Post(db.Model):
    """Post model."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    category = db.Column(db.Enum(PostCategory), default=PostCategory.OTHER)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users_post = db.relationship('User', secondary='user_posts', back_populates='posts')


    def __str__(self):
        return f'<Store: {self.title}>'

    def __repr__(self):
        return f'<Store: {self.title}>'

class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    posts = db.relationship('Post', secondary='user_posts', back_populates='users_post')

    def __str__(self):
        return f'{self.username}'

    def __repr__(self):
        return f'{self.username}'
user_posts = db.Table('user_posts',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'))
)