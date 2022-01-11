from flask_wtf import FlaskForm, RecaptchaField
from wtforms.fields import StringField , PasswordField , SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length , length, EqualTo



class Login(FlaskForm):

    email=EmailField(name='email',
    validators=[Email('Email Is Invalid')])

    password=PasswordField(name='password',
    validators=[DataRequired('Password Field Is Required!'),
    length(min=8, message='Password is Less Than 8 Characters!')])

    recaptcha=RecaptchaField()

    submit=SubmitField()


class Register(FlaskForm):

    firstname=StringField(name='firstname',
    validators=[DataRequired('First Name Field Is Required')])

    lastname=StringField(name='lastname',
    validators=[DataRequired('Last Name Field Is Required')])

    email=EmailField(name='email',
    validators=[DataRequired('Email Is Required!'),
    Email('Email Is Invalid')])

    password=PasswordField(name='password',
    validators=[DataRequired('Password Field Is Required!'),
    Length(min=8, max=12, message='Password Must Be Between 8 and 12 Characers')])

    confirm=PasswordField(name='confirm',
    validators=[DataRequired('Confirm Password Field Is Required!'),
    Length(min=8, max=12, message="Password Must Be Between 8 and 12 Characters"),
    EqualTo('password','Password Does Not Match!!!')])

    recaptcha=RecaptchaField()

    submit=SubmitField()


class EditProfile(FlaskForm):

    firstname=StringField(name='firstname',
    validators=[DataRequired('Name Is Required!')])

    lastname=StringField(name='lastname',
    validators=[DataRequired('Last Name Field Is Required')])

    email=EmailField(name='email',
    validators=[DataRequired('Email Is Required!'),Email('Email Is Invalid!!!')])

    phone=StringField(name='phone',
    validators=[DataRequired('Phone Is Required')])

    bio=StringField(name='bio',
    validators=[Length(max=50, message="Bio Must Be Less Than 50 Characters!")])

    submit=SubmitField('Update Profile')


class ChangePassword(FlaskForm):

    oldPassword=PasswordField(name='oldPassword',
    validators=[DataRequired('Old Password Is Required!'),
    Length(min=8, max=12, message='Password Must Be Between 8 and 12 Characters')])

    newPassword=PasswordField(name='newPassword',
    validators=[DataRequired('New Password Field Is Required!'),
    Length(min=8, max=12, message='Password Must Be Between 8 and 12 Characers')])

    confirm=PasswordField(name='confirm',
    validators=[DataRequired('Confirm Password Field Is Required!'),
    Length(min=8, max=12, message='Password Must Be Between 8 and 12 Characers'),
    EqualTo('newPassword','Password Does Not Match!!!')])

    submit=SubmitField('Change Password')