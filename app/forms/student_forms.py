from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class StForm(FlaskForm):
    id = StringField("Enter ID Number", validators=[DataRequired()])
    firstname = StringField("Enter First Name", validators=[DataRequired()])
    lastname = StringField("Enter Last Name", validators=[DataRequired()])
    year = StringField("Enter Year Level", validators=[DataRequired()])
    gender = StringField("Enter Gender", validators=[DataRequired()])
    course = StringField("Enter Course", validators=[DataRequired()])
    submit = SubmitField("Submit")