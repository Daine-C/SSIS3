from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired

class SearchForm(FlaskForm):
    searched = StringField("Searched", validators=[DataRequired()])
    typs = SelectField(u'Fields', choices=[('al', 'All'),('cl', 'Colleges'),('cr', 'Courses'),('st', 'Students'),('yr', 'Year'),('gen', 'Gender')])
    submit = SubmitField("Submit")
