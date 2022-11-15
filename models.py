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
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(512), nullable=False, default=DEFAULT_IMAGE)

    posts = db.relationship("Post", backref="user")

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

class Post(db.Model):
    """Post class."""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    users = db.relationship('User')