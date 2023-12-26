from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import ValidationError

def FileSizeLimit(max_size_in_mb):
    max_bytes = max_size_in_mb*1024*1024

    def file_length_check(form, field):
        if len(field.data.read()) > max_bytes:
            raise ValidationError(
                f'File size is too large. Max allowed: {max_size_in_mb} MB')
        field.data.seek(0)
    return file_length_check

class ImgForm(FlaskForm):
    pfp = FileField("Profile Picture", validators=[FileRequired(),FileAllowed(['jpg', 'png', 'webp'], 'Images only!'), FileSizeLimit(max_size_in_mb=1)])
    submit = SubmitField("Submit")

