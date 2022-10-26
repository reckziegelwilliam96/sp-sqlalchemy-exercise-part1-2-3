"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add base users
user1 = User(first_name='John', last_name="Smith")
user2 = User(first_name='Jane', last_name="Doe", image_url="https://cdn2.vectorstock.com/i/1000x1000/54/41/young-and-elegant-woman-avatar-profile-vector-9685441.jpg")

# Add new objects to session
db.session.add(user1)
db.session.add(user2)

# Commit
db.session.commit()