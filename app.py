"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_users():
    """Redirect to list of users."""

    return redirect('/users')

@app.route('/users', methods=["GET"])
def show_users_list():
    """Show list of users in home page."""
    # if database is empty, redirect to Create User Page
    if User.query.one_or_none() is None:
        return redirect("newuser.html")
    # else render User List Page
    else:
        users = User.query.order_by(User.last_name, User.first_name).all()
        return render_template("home.html", users=users)
    

@app.route('/users/new', methods = ["GET", "POST"])
def show_new_user_page():
    """Using GET method, Display Create User page: form to add a single user"""
    if request.method == 'GET':
        return render_template("newuser.html")

def add_user():
    """Using POST method, Add user to db.session and redirect to users route to display Users List page."""
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        imageurl = request.form['imageurl']

        user = User(first_name=firstname, last_name=lastname, image_url=imageurl)
        db.session.add(user)
        db.session.commit()

        return redirect('/users')

@app.route('/users/<int:user_id>', methods = ["GET"])
def show_user_details_page(user_id):
    """Show User Details Page: display details on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("userdetail.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def show_edit_user_page(user_id):
    """Show Edit User Page: edit details of a single user"""
    if request.method == 'GET':
        user = User.query.get_or_404(user_id)
        return render_template("useredit.html", user=user)

def update_user_details(user_id):
    """Update user details from database session """
    if request.method == 'POST':
        # Retrieve updated data
        firstname_update = request.form['firstname']
        lastname_update = request.form['lastname']
        imageurl_update = request.form['imageurl']
        # Select user to update from database
        user = User.query.get(user_id)
        # Replace user details with update
        user.first_name = firstname_update
        user.last_name = lastname_update
        user.image_url = imageurl_update
        # add and commit update to database
        db.session.add(user)
        db.session.commit()

        return redirect('/users')

@app.route('/users/<int:user_id>/delete')
def delete_user(user_id):
    """Delete user from database session."""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')