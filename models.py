from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    dietary_preference = db.Column(db.String(50), nullable=False)
    activity_level = db.Column(db.String(50), nullable=False)
    current_weight = db.Column(db.Float)
    target_weight = db.Column(db.Float)  # Make sure this line exists
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    gender = db.Column(db.String(10))

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, username, email, password_hash, dietary_preference="None", activity_level="Low", current_weight=0, goal="None"):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.dietary_preference = dietary_preference
        self.activity_level = activity_level
        self.current_weight = current_weight
        self.goal = goal

    def set_password(self, password):
        """Hash the password before saving it to the database"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the password hash"""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Return the ID of the user as a string for Flask-Login"""
        return str(self.id)

    # Flask-Login expects these methods to be present in the User class.
    def is_authenticated(self):
        """Return True if the user is authenticated, otherwise False"""
        return True  # You may enhance this based on your needs (e.g., adding logic for active sessions)

    def is_active(self):
        """Return True if the user is active, otherwise False"""
        return True  # You can add more logic to check if the user is deactivated, etc.

    def is_anonymous(self):
        """Return True if the user is anonymous, otherwise False"""
        return False  # Since we're using normal users, this should return False