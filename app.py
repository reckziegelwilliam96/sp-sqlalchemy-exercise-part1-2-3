"""Blogly application."""
from flask import Flask, request, render_template, redirect, flash
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy import DateTime
import datetime

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

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("homepage.html", posts=posts)

"""USERS"""

@app.route('/users', methods=["GET"])
def show_users_list():
    """Show list of users in list of users page."""
    users = User.query.order_by(User.last_name, User.first_name).all()
    # if database is empty, redirect to Create User Page
    if len(users) == 0:
        return redirect("newuser.html")
    # else render User List Page
    else:
        return render_template("listuser.html", users=users)
    

@app.route('/users/new', methods = ["GET"])
def show_new_user_page():
    """Using GET method, Display Create User page: form to add a single user"""
    return render_template("newuser.html")

@app.route('/users/new', methods = ["POST"])
def add_user():
    """Using POST method, Add user to db.session and redirect to users route to display Users List page."""
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    imageurl = request.form['image_url']
    user = User(first_name=firstname, last_name=lastname, image_url=imageurl)
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>', methods = ["GET"])
def show_user_details_page(user_id):
    """Show User Details Page: display details on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template("userdetail.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["GET"])
def show_edit_user_page(user_id):
    """Show Edit User Page: edit details of a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("edituser.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user_details(user_id):
    """Update user details from database session """
    # Retrieve updated data
    firstname_update = request.form['first_name']
    lastname_update = request.form['last_name']
    imageurl_update = request.form['image_url']
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

"""POSTS"""

@app.route('/users/<int:user_id>/posts/new', methods = ["GET"])
def show_new_post_page(user_id):
    user = User.query.get(user_id)
    tags = Tag.query.all()
    return render_template("newpost.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods= ["POST"])
def add_post(user_id):
    title = request.form['title']
    content = request.form['content']
    created_at = datetime.datetime.utcnow()
    tags = request.form.getlist('tag')

    post = Post(title=title, content=content, created_at=created_at, user_id=user_id)

    db.session.add(post)
    db.session.commit()
    
    for tag in tags:
        posttag = PostTag(post_id=post.id, tag_id=tag)
    
    db.session.add(posttag)
    db.session.commit()

    return redirect('/users/<int:user_id>', user_id=user_id)

@app.route('/posts/<int:post_id>', methods = ["GET"])
def show_details_post_page(post_id):
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template("postdetail.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["GET"])
def show_edit_post_page(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("editpost.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post_details(post_id):
    """Update Single Post Title, Content and Time. Add to database."""
    title_update = request.form['title']
    content_update = request.form['content']
    created_at_update = datetime.datetime.utcnow()
    tags = request.form.getlist('tag')

    post = Post.query.get(post_id)
    post.title = title_update
    post.content = content_update
    post.created_at = created_at_update

    db.session.add(post)
    db.session.commit()

    for tag in tags:
        tag_update = PostTag(post_id=post_id, tag_id=tag)
    
    db.session.add(tag_update)
    db.session.commit()
    
    return redirect(f'/posts/{ post_id }')

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    """Delete post from database session."""
    post = Post.query.get(post_id)
    user_id = post.user_id

    PostTag.query.filter_by(post_id=post_id).delete()
    #Post.query.filter_by({"id": post_id}).all().delete()

    
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{user_id}')

'''TAGS'''
@app.route('/tags', methods=["GET"])
def list_all_tags():
    """Show Tags List Page"""
    tags = Tag.query.all()

    if len(tags) == 0:
        return redirect('newtag.html')
    else:
        return render_template('listtag.html', tags=tags)

@app.route('/tags/<int:tag_id>', methods = ["GET"])
def show_tag_details_page(tag_id):
    """Show Tag Details Page: display details on a single tag."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tagdetail.html", tag=tag)

@app.route('/tags/new', methods = ["GET"])
def show_new_tag_page():
    """Using GET method, Display Create Tag page: form to add a single tag"""
    return render_template("newtag.html")

@app.route('/tags/new', methods = ["POST"])
def add_tag():
    """Using POST method, Add tag to db.session and redirect to tags route to display tags List page."""
    name = request.form['name']
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=["GET"])
def show_edit_tag_page(tag_id):
    """Show Edit Tag Page: edit details of a single tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("edittag.html", tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def update_tag_details(tag_id):
    """Update tag details from database session """
    # Retrieve updated data
    name_update = request.form['name']
    # Select user to update from database
    tag = Tag.query.get(tag_id)
    # Replace user details with update
    tag.name = name_update
    # add and commit update to database
    db.session.add(tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete')
def delete_tag(tag_id):
    """Delete tag from database session."""
    tag = Tag.query.get(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')