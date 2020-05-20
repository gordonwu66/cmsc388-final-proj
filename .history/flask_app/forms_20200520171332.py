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
        ('CIN','Cincinnati Bengals'),('CLE','Cleveland Browns'),('DAL','Dallas Cowboys'),('DEN','Denver Broncos'),
        ('DET','Detroit Lions'),('GB','Green Bay Packers'),('HOU','Houston Texans'),('IND','Indianapolis Colts'),
        ('JAC','Jacksonville Jaguars'),('KC','Kansas City Chiefs'),('LA','Los Angelos Rams'),('LAC','Los Angelos Chargers'),
        ('MIA','Miami Dolphins'),('MIN','Minnesota Vikings'),('NE','New England Patriots'),('NO','New Orleans Saints'),
        ('NYG','New York Giants'),('NYJ','New York Jets'),('OAK','Oakland Raiders'),('PHI','Philadelphia Eagles'),
        ('PIT','Pittsburgh Steelers'),('SEA','Seattle Seahawks'),('SF','San Francisco 49ers'),('TB','Tampa Bay Buccaneers'),
        ('TEN','Tennessee Titans'),('WAS','Washington Redskins'),('ALL','All Teams')])
    submit = SubmitField('Search')

class PlayerReviewForm(FlaskForm):
    text = TextAreaField('Comment', validators=[InputRequired(), Length(min=1, max=500)])
    draftRound = IntegerField('Draft Round',validators=[InputRequired(),NumberRange(min=1, max=15, message='Draft Round')])
    playAgain = SelectField('Play Again',choices=[('YES','Yes'),('NO','No')])
    submit = SubmitField('Submit Review')

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
