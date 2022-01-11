from app import db
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id=Column(Integer, primary_key=True)
    firstname=Column(String(30))
    lastname=Column(String(30))
    email=Column(String(100))
    password=Column(String(100))
    admin=Column(Boolean(), default=False)
    avatar=Column(String(50), default='/img/avatar.jpg')
    phone=Column(String(20), default='0')
    bio=Column(String(150), default='')
    created_at=Column(DateTime(), default=datetime.utcnow)
    token=Column(String(150), default='')
    

    @property
    def passwd():
        raise AttributeError('Access Forbidden')
    

    @passwd.setter
    def passwd(self,password):
        self.password=generate_password_hash(password)
    

    def IsOriginalPassword(self,user_password):
        return check_password_hash(self.password, user_password)
    


