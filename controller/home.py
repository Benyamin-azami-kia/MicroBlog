from flask import request, render_template, flash, redirect
from flask.helpers import url_for
from controller.post import Post
from models import Article, User
from app import db
from flask_login import current_user


class Home():

    def __init__(self) -> None:
       pass


    def main(self):

        page=request.args.get('page', default=1, type=int)
        articles=Article.Post.query.paginate(page=page, per_page=2)
        categories=db.session.query(Article.Category).all()
        return render_template('main.html',articles=articles, categories=categories)
    


    def viewCategory(self,category_id):
        
        categories=db.session.query(Article.Category).filter_by(id=category_id).first_or_404()
        getArticle=db.session.query(Article.Post).filter_by(category_id=categories.id).all()
        return render_template('Category.html',categories=categories, articles=getArticle)
    


    def single(self,article_id):

        article=Article.Post.query.filter_by(id=article_id).one()
        article.views += 1
        db.session.add(article)
        db.session.commit()
        comments=Article.Comments.query.filter_by(post_id=article_id, status=True)
        user=db.session.query(User.User).filter_by(id=Article.getWriterId(article.writer)).first()
        return render_template('/admin/post/post.html',article=article, comments=comments, user=user)
    


    def sendComment(self,article_id):

        if request.method=='POST':
            if not current_user.is_authenticated :
                flash(message='You Must Log In First!', category='warning')
                return redirect(url_for('single',article_id=article_id))
            else:
                text=request.form['text']
                if text == '':
                    flash(message='Comment Can Not Be Empty!',category='warning')
                    return redirect(url_for('single',article_id=article_id))
                newComment=Article.Comments(user_id=current_user.id, post_id= article_id, text=text)
                db.session.add(newComment)
                db.session.commit()
                flash(message='Comment Sent!', category='info')
                return redirect(url_for('single',article_id=article_id))
    

    def searchItems(self):
        
        ListPosts=[]
        searchInput=request.args.get('search').lower()
        if searchInput == '' or searchInput.isspace() or len(searchInput) < 3 :
            return redirect(url_for('main'))
        posts=Article.Post.query.all()
        for post in posts:
            if searchInput in post.subject.lower() or searchInput in post.content.lower() :
                ListPosts.append(post)
        return render_template('search.html', posts=ListPosts, searchInput=searchInput.capitalize())
    