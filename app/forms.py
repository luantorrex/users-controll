from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember-me: ')
    submit = SubmitField('Login')


class ChangeEmail(FlaskForm):
    email = StringField('Enter a new e-mail: ',
                        validators=[DataRequired(), Email()])
    submit = SubmitField("Change Email")


class ChangePassword(FlaskForm):
    password = PasswordField('Enter a new password',
                             validators=[DataRequired()])
    submit = SubmitField("Change Password")
