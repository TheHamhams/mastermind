from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

login_manager = LoginManager()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# User table
class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    high_score = db.Column(db.Integer, default=0)
    current_streak = db.Column(db.Integer, default=0)
    highest_streak = db.Column(db.Integer, default=0)
    leaderboard = db.relationship('Scores')
    streakboard = db.relationship('Streaks')

    def __init__(self, username, email, password):
        self.id = self.set_id()
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def set_id(self):
        return str(uuid4)

    def __repr__(self):
        return f"{self.username}, {self.email}"

# Scores table for leaderboard
class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)

    def __init__(self, username, user_id, score):
        self.username = username
        self.user_id = user_id
        self.score = score

# Streaks table for streakboard
class Streaks(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    streak = db.Column(db.Integer)

    def __init__(self, username, user_id, streak):
        self.username = username
        self.user_id = user_id
        self.streak = streak