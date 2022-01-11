from app import db, mail
from flask import request, render_template, flash, url_for, redirect
from validators.Auth import Login, Register
from flask_login import login_user, current_user, logout_user
from models import User
from flask_mail import Message
from uuid import uuid4


class Authentication:

    def __init__(self) -> None:
        pass


    def signin(self):
        if current_user.is_authenticated:
            return redirect(url_for('main'))


        form=Login()
        if request.method == 'POST':
            if form.validate():
                email=request.form.get('email')
                password=request.form.get('password')
                user=User.User.query.filter_by(email=email).first()
                if not user:
                    flash(message='User Not Exist!', category='danger')
                    return redirect(url_for('signin'))
                if user.IsOriginalPassword(password):
                    login_user(user)
                    next_page=request.args.get('next')
                    if current_user.admin:
                        return redirect(url_for('admin')) if next_page else redirect(url_for('main'))
                    else:
                        return redirect(url_for('account')) if next_page else redirect(url_for('main'))
                else:
                    flash(message='Password or Email Is Wrong', category='danger')
                    return redirect(url_for('signin'))
        return render_template('./auth/signin.html',form=form)


    def signup(self):
        if current_user.is_authenticated:
            return redirect(url_for('main'))
        
        form=Register()
        if request.method == 'POST':
            if form.validate():
                firstname=request.form['firstname']
                lastname=request.form['lastname']
                email=request.form['email']
                password=request.form['password']
                user=User.User.query.filter_by(email=email).first()
                if not user :
                    newuser=User.User(firstname=firstname,lastname=lastname,email=email,passwd=password)
                    db.session.add(newuser)
                    result=db.session.commit()
                    if result != False:
                        flash(message="New User Added",category="success")
                        return redirect(url_for('signup'))
                    else:
                        flash(message='Server Error! Please Try again Later!', category='danger')
                else:
                    flash(message='User Exists, Please Enter another Email',category='danger')
                    return redirect(url_for('signup'))
        return render_template('./auth/signup.html',form=form)
    

    def forgetPassword(self):

        if current_user.is_authenticated:
            return redirect(url_for('main'))
        if request.method == 'POST' :
            if request.form.get('email') == '' :
                flash(message='Email Is Empty!',category='warning')
                return redirect(url_for('forgetPassword'))
            email = request.form.get('email')
            user=db.session.query(User.User).filter_by(email = email).first()
            if not user:
                flash(message='There Is No User By That Email', category='danger')
                return redirect(url_for('forgetPassword'))
            user.token=str(uuid4())
            db.session.add(user)
            db.session.commit()

            msg=Message(subject='Reset Password (Py MicroBlog)', recipients=['benyamin@smtp.mailtrap.io'], sender='tosmtp.mailtrap.io')
            msg.body='Please Click On this Link to Reset Your Password'
            msg.html=f'''<a href="http://127.0.0.1:5000/resetPassword/{user.token}/{user.id}">Reset Password</a>'''

            mail.send(msg)
            flash(message='Email Sent !', category='success')
            return redirect(url_for('forgetPassword'))
        return render_template('/auth/forgetpassword.html')
    

    def resetPassword(self,user_token, user_id):

        if current_user.is_authenticated:
            return redirect(url_for('main'))
        if request.method == 'POST':
            if request.form.get('password') == '' and len(request.form.get('password')) < 8 :
                flash(message='Please Check Password Field!', category='warning')
                return redirect(url_for('resetPassword',user_token=user_token, user_id=user_id))
            user=db.session.query(User.User).filter_by(id=user_id, token=user_token).first()
            if user:
                user.passwd=request.form.get('password')
                user.token=''
                db.session.commit()
                return redirect(url_for('signin'))
        return render_template('/auth/resetpassword.html',user_token=user_token,user_id=user_id)            
            
    
    
    def signout(self):
        if current_user:
            logout_user()
        return redirect(url_for('main'))
