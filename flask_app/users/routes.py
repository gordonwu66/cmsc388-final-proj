from flask import render_template, request, redirect, url_for, flash, Response
from flask import Blueprint
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

from flask_app import app, bcrypt, client
from flask_app.forms import (PlayerReviewForm, RegistrationForm, LoginForm, UpdateUsernameForm)
from flask_app.models import User, Review, load_user
from flask_app.utils import current_time

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed)

        user.save()

        session['new_username'] = user.username

        return redirect(url_for('users.tfa'))

    return render_template('register.html', title='Register', form=form)


@users.route('/qr_code')
def qr_code():
    if 'new_username' not in session:
        return redirect(url_for('main.index'))

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

@users.route('/tfa')
def tfa():
    if 'new_username' not in session:
        return redirect(url_for('main.index'))

    headers = {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }
    return render_template('tfa.html'), headers

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.objects(username = form.username.data).first()

        if (user is not None and
            bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user)

            return redirect(url_for('users.account'))


    return render_template('login.html', title = 'Login', form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateUsernameForm()

    if form.validate_on_submit():
        # update username field in db

        current_user.modify(username=form.username.data)
        current_user.save()

        return redirect(url_for('users.account'))

    return render_template('account.html', form=form)