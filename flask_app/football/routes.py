from flask import render_template, request, redirect, url_for, flash, Response
from flask import Blueprint
from flask import session

from flask_mongoengine import MongoEngine
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

# stdlib
from datetime import datetime

from flask_app import app, bcrypt, client
from flask_app.forms import (PlayerReviewForm)
from flask_app.models import User, Review, load_user
from flask_app.utils import current_time

football = Blueprint('football', __name__)


@football.route('/team-results/<query>', methods=['GET'])
def team_results(query):
    print(query)
    if query=='ALL':
        results = client.all_players()
    else:
        results = client.get_players_by_team(query)

    if type(results) == dict:
        return render_template('query.html', error_msg=results['error'])
    
    return render_template('query.html', results=results)

@football.route('/player-results/<fname>_<lname>', methods=['GET'])
def player_results(fname, lname):
    print(fname+lname)
    fullname = fname + lname
    if len(fullname) == 0:
        results = client.all_players()
    else:
        player = client.retrieve_player_by_name(fname, lname)
        if type(player) == dict:
            return render_template('player_detail.html', error_msg=player['error'])
        else:
            return redirect(url_for('football.player_detail', player_id=player))

    if type(results) == dict:
        return render_template('query.html', error_msg=results['error'])
    
    return render_template('query.html', results=results)

@football.route('/players/<player_id>', methods=['GET', 'POST'])
def player_detail(player_id):
    result = client.retrieve_player_by_id(player_id)

    if type(result) == dict:
        return render_template('player_detail.html', error_msg=result['error'])

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