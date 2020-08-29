from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class RegistrationForm(FlaskForm):
    username = StringField('Username: ', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
