# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_talisman import Talisman
from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

# stdlib
import os
from datetime import datetime

# local
from .client import PlayerClient

app = Flask(__name__)

# Flask-Talisman
# Ensure all traffic is loaded with HTTPS (secure connection) by using 'self'
csp = {
    'default-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'stackpath.bootstrapcdn.com',
        'code.jquery.com',
        'cdn.jsdelivr.net'
    ]
}
Talisman(app, content_security_policy=csp)

app.config["MONGODB_HOST"] = 'mongodb://heroku_1g94z7ls:6jah3cqn8h46fqlogsjfhhic9m@ds161109.mlab.com:61109/heroku_1g94z7ls?retryWrites=false'
#app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/finalproject'
app.config['SECRET_KEY'] = b'\x020;yr\x91\x11\xbe"\x9d\xc1\x14\x91\xadf\xec'

# mongo = PyMongo(app)
db = MongoEngine(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
bcrypt = Bcrypt(app)

client = PlayerClient()

from flask_app.main.routes import main  # Blueprint class
from flask_app.users.routes import users
from flask_app.football.routes import football

app.register_blueprint(main)
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(football)