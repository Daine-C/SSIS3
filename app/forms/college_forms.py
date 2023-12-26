from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class ClForm(FlaskForm):
    id = StringField("Enter College Code", validators=[DataRequired()])
    name = StringField("Enter College Name", validators=[DataRequired()])
    submit = SubmitField("Submit")