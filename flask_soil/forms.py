from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_soil.model import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=24)])
    password = PasswordField('Password', validators = [DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    first_name=StringField('First Name', validators=[DataRequired(), Length(min=2, max=24)])
    last_name=StringField('Last Name', validators=[DataRequired(), Length(min=2, max=24)])
    name_of_farm=StringField('Name of Farm', validators=[DataRequired(), Length(min=2, max=24)])
    username =StringField('Username', validators=[DataRequired(), Length(min=2, max=24)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        userf = User.query.filter_by(username=username.data).first()
        if userf:
            raise ValidationError('Username taken. Please choose another')

    def validate_email(self, email):
        userf = User.query.filter_by(email=email.data).first()
        if userf:
            raise ValidationError('Email taken. Please choose another')
