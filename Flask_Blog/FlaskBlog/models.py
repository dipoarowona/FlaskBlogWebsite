# -*- coding: utf-8 -*-
from datetime import datetime
from FlaskBlog import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as  Serializer #this is for a timed token to reset password via email
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


#one to many relationship 
#- one user can have many post but a one post can only have one user

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    profile_image = db.Column(db.String(20), nullable = False, default = "default.jpg")
    password = db.Column(db.String(60), nullable = False)
    post = db.relationship('Post', backref = "author", lazy = True)
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec) 
        
        return s.dumps({'user_id' : self.id}).decode("utf-8")#returns a token decoded with an expiration of 30 minutese
    
    @staticmethod #tells python that it is a static metho    
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        
        try:
            user_id = s.loads(token)["user_id"]  #try and load id
        except:
            return None
        
        return User.query.get(user_id)

    def __repr__(self):#how the object is printed when we print it out
        return f"User('{self.username}','{self.email}','{self.profile_image}')"
    
    
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),nullable = False,)
    time = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    content = db.Column(db.Text, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.time}')"
