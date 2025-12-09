from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class DatasetForm(FlaskForm):
    name = StringField(
        "KB Name",
        validators=[
            DataRequired(message="KB name is required."),
            Length(max=20, message="KB name cannot exceed 20 characters.")
        ],
    )
    desc = TextAreaField(
        "KB Description",
        validators=[
            DataRequired(message="KB description is required."),
            Length(max=200, message="KB description cannot exceed 200 characters.")
        ],
    )

class SegmentForm(FlaskForm):
    content = TextAreaField(
        "Content",
        validators=[
            DataRequired(message="Content is required."),
            Length(min=5, max=2000, message="Content must be between 5 and 2000 characters.")
        ],
    )
    order = IntegerField(
        "Order",
        validators=[
            DataRequired(message="Order is required."),
            NumberRange(min=1, message="Order must be a positive integer.")
        ],
    )