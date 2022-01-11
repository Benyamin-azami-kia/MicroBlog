from flask_wtf import FlaskForm
from wtforms.fields import StringField , PasswordField , SubmitField, EmailField
from wtforms.validators import DataRequired, Email, Length , length, EqualTo



class CreateUser(FlaskForm):

    firstname=StringField(name='firstname',
    validators=[DataRequired('First Name Is Required!')])

    lastname=StringField(name='lastname',
    validators=[DataRequired('Last Name Is Required!')])

    email=EmailField(name='email',
    validators=[DataRequired('Email Is Required!'),
    Email('Email Is Invalid!')])

    password=PasswordField(name='password',
    validators=[DataRequired('Password Field Is Required!'),
    Length(min=8, max=12, message='Password Must Be Between 8 and 12 Characers')])

    confirm=PasswordField(name='confirm',
    validators=[DataRequired('Confirm Password Field Is Required!'),
    Length(min=8, max=12, message="Password Must Be Between 8 and 12 Characters"),
    EqualTo('password','Password Does Not Match!!!')])

    submit=SubmitField('Create User')


class EditUser(FlaskForm):

    firstname=StringField(name='firstname',
    validators=[DataRequired('First Name Is Required!')])

    lastname=StringField(name='lastname',
    validators=[DataRequired('Last Name Is Required!')])

    email=EmailField(name='email',
    validators=[DataRequired('Email Is Required!'),
    Email('Email Is Invalid!')])

    phone= StringField(name='phone',
    validators=[DataRequired('Phone Is Required!')])

    submit=SubmitField('Edit User Account')