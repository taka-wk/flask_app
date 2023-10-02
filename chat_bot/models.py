from datetime import datetime
from pytz import timezone

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin

from chat_bot import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#ユーザー情報
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
    
    def __repr__(self):
        return f"UserName: {self.username}"
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)