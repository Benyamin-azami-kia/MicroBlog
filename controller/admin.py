from app import db, allow_file_type, app
from flask import request, render_template, flash, url_for, redirect
from flask_login import current_user, login_required
from validators.Auth import EditProfile, ChangePassword
from validators.Admin import CreateUser, EditUser
from werkzeug.utils import secure_filename
from models import User, Article
import os

class Admin:

    def __init__(self) -> None:
       pass



    @login_required
    def adminAccount(self):

        if not current_user.admin:
            return redirect(url_for('account'))
        rows=Article.Comments.query.filter_by(status=False).count()
        return render_template('/admin/admin.html',rows=rows)



    @login_required
    def admin_info(self):
        if not current_user.admin:
            return redirect(url_for('account'))
        return render_template('/admin/admin_info.html')



    @login_required
    def admin_account_edit(self):
        if not current_user.admin:
            return redirect(url_for('account'))
        form=EditProfile()
        if request.method == 'POST':
            if form.validate():
                firstname=request.form.get('firstname')
                lastname=request.form.get('lastname')
                email=request.form.get('email')
                phone=request.form.get('phone')
                bio=request.form.get('bio')
                user=db.session.query(User.User).filter_by(email=current_user.email).one()
                user.firstname=firstname
                user.lastname=lastname
                user.email=email
                user.bio=bio
                user.phone=phone
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('admin_info'))
        return render_template('/admin/admin_account_edit.html', form=form)



    @login_required
    def admin_change_password(self):
        if not current_user.admin:
            return redirect(url_for('account'))

        form=ChangePassword()
        if request.method == 'POST' :
            if form.validate():
                oldPassword=request.form.get('oldPassword')
                user=db.session.query(User.User).filter_by(email=current_user.email).one()
                if not user.IsOriginalPassword(oldPassword):
                    flash(message='Old Password Is Incorrect!')
                    return redirect(url_for('change_password'))
                else:
                    newPassword=request.form.get('newPassword')
                    user.passwd=newPassword
                    db.session.add(user)
                    db.session.commit()
                    flash(message='Password Changed Successfully',category='success')
                    return redirect(url_for('admin_change_password'))
        return render_template('/admin/admin_change_password.html',form=form)



    @login_required
    def admin_upload_avatar(self):
        if not current_user.admin:
            return redirect(url_for('account'))
            
        if request.method == 'POST' :
            avatar=request.files['avatar']
            filename=avatar.filename
            filesecure=secure_filename(filename)
            if not allow_file_type(filename):
                flash(message='File Type Is Not Supported!',category='danger')
                return redirect(url_for('admin_upload_avatar'))
            avatar.save(os.path.join(app.config['UPLOAD_DIR'],filesecure))
            user=db.session.query(User.User).filter_by(email=current_user.email).one()
            user.avatar=f'/uploads/{filename}'
            db.session.add(user)
            db.session.commit()
            flash(message='Photo Uploaded Successfully', category='success')
            return redirect(url_for('admin_upload_avatar'))
        return render_template('/admin/admin_avatar.html')



    @login_required
    def userList(self):

        if not current_user.admin:
            return redirect(url_for('account'))
        if request.method == 'POST' :
            user=User.User.query.filter_by(id=request.args.get('id')).one()
            db.session.delete(user)
            db.session.commit()
        get_user_list=User.User.query.all()
        return render_template('/admin/user/userlist.html',users=get_user_list)
    


    @login_required
    def admin_create_user(self):

        if not current_user.admin:
            return redirect(url_for('account'))
        form = CreateUser()
        if request.method == 'POST' :
            if form.validate():
                firstname=request.form['firstname']
                lastname=request.form['lastname']
                email=request.form['email']
                password=request.form['password']
                user=User.User.query.filter_by(email=email).first()
                if user:
                    flash(message='User Is Already Exist!', category='danger')
                    return redirect(url_for('admin_create_user'))
                else:
                    user=User.User(firstname=firstname, lastname=lastname, email=email, passwd=password)
                    db.session.add(user)
                    db.session.commit()
                    flash(message='User Added!',category='success')
                    return redirect(url_for('admin_create_user'))
        return render_template('/admin/user/createuser.html',form=form)



    @login_required
    def admin_edit_user(self):
        
        if not current_user.admin:
            return redirect(url_for('account'))
        form=EditUser()
        user=User.User.query.filter_by(id=request.args.get('id')).first()
        if request.method == 'POST':
            if form.validate():
                firstname=request.form['firstname']
                lastname=request.form['lastname']
                email=request.form['email']
                phone=request.form['phone']
                user.firstname=firstname
                user.lastname=lastname
                user.email=email
                user.phone=phone
                db.session.commit()

                flash(message='User Updated!',category='success')
                return redirect(url_for('admin_edit_user'))
        return render_template('/admin/user/admin_user_edit.html',form=form, user=user)

    
    @login_required
    def commentList(self):

        if not current_user.admin:
            return redirect(url_for('account'))
        
        if request.method == 'POST':
            Article.Comments.query.filter_by(id=request.args.get('id')).delete()
            db.session.commit()
            return redirect(url_for('commentList'))
        comments=Article.Comments.query.all()
        return render_template('/admin/commentList.html', comments=comments)
    

    @login_required
    def approveComment(self, comment_id):

        if not current_user.admin:
            return redirect(url_for('account'))
        
        if request.method == 'POST':
            comment=Article.Comments.query.filter_by(id=comment_id).one()
            comment.status=True
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('commentList'))
            
    


