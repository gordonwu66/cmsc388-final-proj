# 3rd-party packages
from flask import render_template, request, redirect, url_for, flash, Response

from flask import session
import pyotp
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64

from flask_sqlalchemy import SQLAlchemy

from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
from datetime import datetime

# local
from . import app, bcrypt, client
from .forms import (SearchForm, PlayerReviewForm, RegistrationForm, LoginForm,
                             UpdateUsernameForm)
from .models import User, Review, load_user
from .utils import current_time

""" ************ View functions ************ """
@app.route('/', methods=['GET', 'POST'])
def index():

    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for('query_results', query=form.search_query.data))

    return render_template('index.html', form = form)

@app.route('/search-results/<query>', methods=['GET'])
def query_results(query):
    print(query)
    if query=='ALL':
        results = client.all_players()
    else:
        results = client.get_players_by_team(query)

    if type(results) == dict:
        return render_template('query.html', error_msg=results['Error'])
    
    return render_template('query.html', results=results)


@app.route('/players/<player_id>', methods=['GET', 'POST'])
def player_detail(player_id):
    result = client.retrieve_player_by_id(player_id)

    if type(result) == dict:
        return render_template('player_detail.html', error_msg=result['Error'])

    form = PlayerReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=load_user(current_user.username), 
            content=form.text.data,
            draftRound=form.draftRound.data,
            playAgain=form.playAgain.data, 
            date=current_time(),
            player_id=player_id,
            player_name=result.fullname
        )

        review.save()

        return redirect(request.path)

    reviews = Review.objects(player_id=player_id)

    print(current_user.is_authenticated)

    return render_template('player_detail.html', form=form, player=result, reviews=reviews)

@app.route('/user/<username>')
def user_detail(username):

    # Create list of reviews done by the specified user
    reviews = Review.objects(commenter=User.objects(username=username).first())
    return render_template('user_detail.html', username = username, reviews = reviews)


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed)

        user.save()

        session['new_username'] = user.username

        return redirect(url_for('tfa'))

    return render_template('register.html', title='Register', form=form)


@app.route('/qr_code')
def qr_code():
    if 'new_username' not in session:
        return redirect(url_for('index'))

    #user = User.query.filter_by(username=session['new_username']).first()
    user = User.objects(username = session['new_username']).first()
    session.pop('new_username')

    uri = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(name=user.username, issuer_name='Fantasy-Football')
    img = qrcode.make(uri, image_factory= qrcode.image.svg.SvgPathImage)
    stream = BytesIO()
    img.save(stream)

    headers = {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }

    return stream.getvalue(), headers

@app.route('/tfa')
def tfa():
    if 'new_username' not in session:
        return redirect(url_for('index'))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    return render_template('tfa.html'), headers

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username = form.username.data).first()

        if (user is not None and
            bcrypt.check_password_hash(user.password, form.password.data)):
            print('HERE!')
            login_user(user)

            return redirect(url_for('account'))
        else:
            print('WTF!')
    else:
        print("EVEN MORE WTF")
    return render_template('login.html', title = 'Login', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUsernameForm()

    if form.validate_on_submit():
        # update username field in db

        current_user.modify(username=form.username.data)
        current_user.save()

        return redirect(url_for('account'))

    return render_template('account.html', form=form)
