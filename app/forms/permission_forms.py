from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PermissionForm(FlaskForm):
    code = StringField("Code", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    module = StringField("Module", validators=[DataRequired()])
    description = TextAreaField("Description")
    submit = SubmitField("Save")
