from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="TestUser", last_name="TestUser")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>TestUser</h1>', html)

    def test_add_user(self):
        with app.test_client() as client:
            user2 = {"first_name": "TestUser2", "last_name": "TestUser2", "image_url": "https://st.depositphotos.com/2218212/2938/i/950/depositphotos_29387653-stock-photo-facebook-profile.jpg'"}
            resp = client.post("/users/new", data=user2, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<h1>TestUser2</h1>", html)
    
    def test_delete_user(self):
        user3 = {"first_name": "TestUser3", "last_name": "TestUser3", "image_url": "https://st.depositphotos.com/2218212/2938/i/950/depositphotos_29387653-stock-photo-facebook-profile.jpg'"}
        db.session.add(user3)
        db.session.commit()
        with app.test_client() as client:
            resp = client.get(f'/users/{self.user3.id}/delete', follows_redirects=True)
            html = resp.get_date(as_text=True)

            self.asserEqual(resp.status_code, 200)
            self.assertNotIn('TestUser3', html)


class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""
    def setUp(self):
        """Add sample post with user test."""
        user = User(first_name="TestUser4", last_name="TestUser4")
        post = Post(title="TestPostTitle", content="TestPostContent", user=user)
        db.session.add(user)
        db.session.add(post)
        db.session.commit()

        self.user_id = user.id
        self.post_id = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()