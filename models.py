"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

DEFAULT_IMAGE = 'https://st.depositphotos.com/2218212/2938/i/950/depositphotos_29387653-stock-photo-facebook-profile.jpg'

class User(db.Model):
    """User class."""
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, nullable=False, default=DEFAULT_IMAGE)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def get_full_name(self):
       return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Post class."""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    users = db.relationship('User', backref="post")
    tags = db.relationship('Tag', secondary="post_tags", backref="post")

    @property
    def user_date(self):
        return self.created_at.strftime("%a, %d %b, %Y %H:%M:%S")

class Tag(db.Model):
    """Tag Model."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True, nullable=False)

    posts = db.relationship('Post', secondary="post_tags", cascade="all, delete", backref="tag")

class PostTag(db.Model):
    """PostTag Model."""

    __tablename__ = "post_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    