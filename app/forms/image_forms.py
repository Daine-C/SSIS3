from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from flask_wtf.file import FileAllowed

class ImgForm(FlaskForm):
    pfp = FileField("Profile Picture", validators=[FileAllowed(['jpg', 'png', 'webp'], 'Images only!')])
    submit = SubmitField("Submit")