from app import db
from sqlalchemy import Column, String, Integer, Text, ForeignKey, Boolean, DateTime
from datetime import datetime
from . import User

class Post(db.Model):

    id=Column(Integer, primary_key=True)
    subject=Column(String(50))
    content=Column(Text)
    thumb=Column(String(100),default='')
    writer=Column(Integer, ForeignKey('user.id'))
    publish=Column(Boolean, default=False)
    category_id=Column(Integer, ForeignKey('category.id'))
    views=Column(Integer, default=0)
    created_at=Column(DateTime, default=datetime.utcnow())


    def getWriter(self):
        
        user=User.User.query.filter_by(id=self.writer).first()
        return user.firstname +' '+ user.lastname


class Comments(db.Model):

    id=Column(Integer,primary_key=True)
    user_id=Column(Integer, ForeignKey('user.id'))
    post_id=Column(Integer, ForeignKey('post.id'))
    text=Column(Text)
    status=Column(Boolean, default=False)
    created_at=Column(DateTime, default=datetime.utcnow())


    def getWriter(self):
        
        user=User.User.query.filter_by(id=self.user_id).first()
        return user.firstname +' '+ user.lastname
    
    def getArticle(self):

        post=Post.query.filter_by(id=self.post_id).first()
        return post.subject



class Category(db.Model):

    id = Column(Integer, primary_key=True)
    name=Column(String(150))


def getWriterId(article_id):

        userId=User.User.query.filter_by(id=article_id).first()
        return userId.id
