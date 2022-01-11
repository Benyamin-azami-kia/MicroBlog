from app import db, allow_file_type, app
from flask import request, redirect, render_template, flash, url_for
from validators.Article import CreatePost, EditPost, EditCategory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
from models import Article
from flask_login import login_required, current_user


class Post:

    def __init__(self) -> None:
        pass
    

    @login_required
    def createPost(self):

        if not current_user.admin:
            return redirect(url_for('account'))
        form=CreatePost()
        categories=Article.Category.query.all()
        if request.method == 'POST':
            if form.validate():
                subject=request.form.get('subject')
                category_id=request.form.get('category')
                content=request.form.get('content')
                publish= True if request.form.get('publish') == 'on' else False
                thumb=request.files['thumb'] if 'thumb' in request.files else None
                if thumb is not None and allow_file_type(thumb.filename):
                    thumb.save(os.path.join(app.config['UPLOAD_DIR'], secure_filename(thumb.filename)))
                newPost=Article.Post(subject=subject,category_id=category_id,content=content,publish=publish,writer=current_user.id, thumb=str(f'/uploads/{thumb.filename}'))
                db.session.add(newPost)
                db.session.commit()
                flash(message='New Post Created!',category='warning')
                return redirect(url_for('createPost'))
        return render_template('/admin/post/create.html',form=form, categories=categories)
    

    @login_required
    def postList(self):

        if not current_user.admin:
            return redirect(url_for('account'))
        
        if request.method == 'POST':
            Article.Post.query.filter_by(id=request.args.get('id')).delete()
            db.session.commit()
            return redirect(url_for('postList'))
        article=Article.Post.query.all()
        return render_template('/admin/post/postlist.html',articles=article)
    

    @login_required
    def editPost(self):
        
        if not current_user.admin:
            return redirect(url_for('account'))
        categories=Article.Category.query.all()
        article=Article.Post.query.filter_by(id=request.args.get('id')).one()
        form=EditPost()
        if request.method == 'POST' :
            if form.validate() :
                subject=request.form.get('subject')
                category_id=request.form.get('category')
                content=request.form.get('content')
                thumb=request.files['thumb'] if request.files['thumb'].filename != '' else article.thumb
                publish= True if request.form.get('publish') == 'on' else False
                if isinstance(thumb,FileStorage):
                    thumb.save(os.path.join(app.config['UPLOAD_DIR'],secure_filename(thumb.filename)))
                    article.thumb='/uploads/'+thumb.filename
                if content =='':
                    flash(message='Content Is Empty!',category='warning')
                    return redirect(url_for('editPost'))
                article.subject=subject
                article.category_id=category_id
                article.content=content
                article.publish=publish
                db.session.add(article)
                db.session.commit()
                return redirect(url_for('postList'))
        return render_template('/admin/post/edit.html',form=form ,categories=categories ,article=article)


    @login_required
    def createCategory(self):
        
        if not current_user.admin:
            return redirect(url_for('account'))

        if request.method == 'POST' :
            name=request.form.get('name')
            if name=='':
                flash(message='Category Name Is Empty!', category='warning')
                return redirect(url_for('createCategory'))
            newCategory=Article.Category(name=name)
            db.session.add(newCategory)
            db.session.commit()
            flash(message='New Category Created!', category='success')
            return redirect(url_for('createCategory'))
        return render_template('/admin/category/createCategory.html')
    

    @login_required
    def categories(self):
        
        if not current_user.admin:
            return redirect(url_for('account'))
        
        if request.method=='POST':
            category_id=request.args.get('id')
            Article.Category.query.filter_by(id=category_id).delete()
            db.session.commit()
            return redirect(url_for('categories'))
        
        categories=db.session.query(Article.Category).all()
        return render_template('/admin/category/category.html', categories=categories)
    

    @login_required
    def editCategory(self):

        if not current_user.admin:
            return redirect(url_for('account'))
        category=Article.Category.query.filter_by(id=request.args.get('id')).one()
        form=EditCategory()
        if request.method == 'POST' :
            if form.validate() :
                name=request.form.get('name')
                category.name=name
                db.session.commit()
                return redirect(url_for('categories'))
                 
            else:
                flash(message='Name Is Empty!', category='warning')
                return redirect(url_for('editCategory'))
                  
        return render_template('/admin/category/editCategory.html',form=form, category=category)