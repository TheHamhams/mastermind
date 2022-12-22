from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    active = db.Column(db.Boolean, default=False)
    current = db.Column(db.Integer)
    
    def __init__(self, username, email, password):
        self.id = self.set_id()
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
    
    def set_id(self):
        return str(uuid4)

    def __repr__(self):
        return f"{self.username}, {self.email}"
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'username', 'email', 'password', 'active', 'current']
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)

class Scores(db.Model):
    id = db.Column(db.String(), primary_key=True)
    username = db.Column(db.String(15))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Integer)