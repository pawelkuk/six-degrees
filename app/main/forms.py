from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class WikiNodesForm(FlaskForm):
    source = StringField(label="Source site", validators=[DataRequired()])
    target = StringField(label="Destination site", validators=[DataRequired()])
    submit = SubmitField(label="Search")
