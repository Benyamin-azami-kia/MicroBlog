from app import db, allow_file_type, app
from flask import request, render_template, flash, url_for, redirect
from flask_login import login_user, current_user, logout_user, login_required
from validators.Auth import EditProfile, ChangePassword
from werkzeug.utils import secure_filename
from models import User
import os


class Account:

    def __init__(self) -> None:
        pass
    
    @login_required
    def account(self):
        if current_user.admin:
            return redirect(url_for('adminAccount'))
        return render_template('/account/account.html')


    @login_required
    def account_info(self):
        if current_user.admin:
            return redirect(url_for('adminAccount'))
        return render_template('/account/info.html')


    @login_required
    def account_edit(self):
        if current_user.admin:
            return redirect(url_for('adminAccount'))
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
                return redirect(url_for('account_info'))
        return render_template('/account/edit.html', form=form)


    @login_required
    def change_password(self):
        if current_user.admin:
            return redirect(url_for('adminAccount'))

        form=ChangePassword()
        if request.method == 'POST' :
            if form.validate():
                oldPassword=request.form.get('oldPassword')
                user=db.session.query(User.User).filter_by(email=current_user.email).one()
                if not user.IsOriginalPassword(oldPassword):
                    flash(message='Old Password Is Incorrect!', category='warning')
                    return redirect(url_for('change_password'))
                else:
                    newPassword=request.form.get('newPassword')
                    user.passwd=newPassword
                    db.session.add(user)
                    db.session.commit()
                    flash(message='Password Changed Successfully',category='success')
                    return redirect(url_for('change_password'))
        return render_template('/account/changepassword.html',form=form)

    
    @login_required
    def upload_avatar(self):
        if current_user.admin:
            return redirect(url_for('adminAccount'))
            
        if request.method == 'POST' :
            avatar=request.files['avatar']
            filename=avatar.filename
            filesecure=secure_filename(filename)
            if not allow_file_type(filename):
                flash(message='File Type Is Not Supported!',category='danger')
                return redirect(url_for('upload_avatar'))
            avatar.save(os.path.join(app.config['UPLOAD_DIR'],filesecure))
            user=db.session.query(User.User).filter_by(email=current_user.email).one()
            user.avatar=f'/uploads/{filename}'
            db.session.add(user)
            db.session.commit()
            flash(message='Photo Uploaded Successfully', category='success')
            return redirect(url_for('upload_avatar'))
        return render_template('/account/avatar.html')