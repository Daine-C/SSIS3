from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CrForm(FlaskForm):
    id = StringField("Enter Course Code", validators=[DataRequired()])
    name = StringField("Enter Course Name", validators=[DataRequired()])
    collg = StringField("Enter College", validators=[DataRequired()])
    submit = SubmitField("Submit")