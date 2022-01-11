from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired


class CreatePost(FlaskForm):

    subject=StringField(name='subject',
    validators=[DataRequired('Subject Is Reauired!')])

    content=TextAreaField(name='content',
    validators=[DataRequired('Content Is Required!')])

    thumb=FileField()

    submit=SubmitField('Create New Post')


class EditPost(FlaskForm):

    subject=StringField(name='subject',
    validators=[DataRequired('Subject Is Reauired!')])

    thumb=FileField()

    submit=SubmitField('Update Post')


class EditCategory(FlaskForm):

    name=StringField(name='name',
    validators=[DataRequired('Name Is Reauired!')])

    submit=SubmitField('Update')
    

