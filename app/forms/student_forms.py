from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class StForm(FlaskForm):
    id = StringField("Enter ID Number", validators=[DataRequired(),Length(min=9, max=9)])
    firstname = StringField("Enter First Name", validators=[DataRequired()])
    lastname = StringField("Enter Last Name", validators=[DataRequired()])
    year = StringField("Enter Year Level", validators=[DataRequired()])
    gender = StringField("Enter Gender", validators=[DataRequired()])
    course = StringField("Enter Course", validators=[DataRequired()])
    submit = SubmitField("Submit")