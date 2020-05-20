from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import (InputRequired, DataRequired, NumberRange, Length, Email, 
                                EqualTo, ValidationError)


from .models import User

class SearchForm(FlaskForm):
    search_query = SelectField('Query', choices=[('ARI','Arizona Cardinals'), ('ATL','Atlanta Falcons'),
        ('BAL','Baltimore Ravens'),('BUF','Buffalo Bills'),('CAR','Carolina Panthers'), ('CHI','Chicago Bears'),
        ('CIN','Cincinnati Bears') - CLE - DAL - DEN - DET - GB - HOU - IND - JAC - KC - LA - LAC - LV - MIA - MIN - NE - NO - NYG - NYJ - OAK - PHI - PiT - SD - SEA - SF - STL - TB - TEN - WAS')])
    submit = SubmitField('Search')

class PlayerReviewForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(min=1, max=500)])
    submit = SubmitField('Enter Comment')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=1, max=40)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')

    def validate_email(self, email):        
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError('Email is taken')

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min = 1, max=40)])
    password = PasswordField('Password', validators=[InputRequired()])

    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.objects(username = username.data).first()
        if user is None:
            raise ValidationError('Login failed. Check your username and/or password')

    def validate_password(self, password):
        user = User.objects(password = password.data).first()
        if user is None:
            raise ValidationError('Login failed. Check your username and/or password')

class UpdateUsernameForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired(), Length(min = 1, max=40)])

    submit = SubmitField('Update Username')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError('Username is taken')

class UpdateProfilePicForm(FlaskForm):
    pass
