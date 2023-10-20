from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from flask_wtf.file import FileField

class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")

class ClForm(FlaskForm):
    id = StringField("Enter College Code", validators=[DataRequired()])
    name = StringField("Enter College Name", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CrForm(FlaskForm):
    id = StringField("Enter information", validators=[DataRequired()])
    name = StringField("Enter information", validators=[DataRequired()])
    submit = SubmitField("Submit")

class StForm(FlaskForm):
    info = StringField("Enter information", validators=[DataRequired()])
    submit = SubmitField("Submit")