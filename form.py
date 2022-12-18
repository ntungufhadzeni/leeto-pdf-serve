from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import (
    StringField,
    DateField,
    SubmitField,
)

from wtforms.validators import (
    DataRequired,
    InputRequired
)


class AnnouncementForm(FlaskForm):
    title = StringField(
        'Title',
        [
            DataRequired(message="Title is required")
        ]
    )
    date = DateField(
        'Date',
        [
            DataRequired(message="Date is required")
        ]
    )
    upload = FileField('Media', validators=[
        FileRequired(message="Please choose a file"),
        FileAllowed(('jpg', 'pdf', 'png'), 'Only jpg, pdf, png allowed')
    ])
    submit = SubmitField('Post')




