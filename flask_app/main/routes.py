from flask import render_template, request, redirect, url_for, flash, Response
from flask import Blueprint
from flask_app.forms import (SearchTeamForm, SearchPlayerForm)
from flask_app.models import User, Review

main = Blueprint("main", __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    form = SearchTeamForm()
    form2 = SearchPlayerForm()

    if form.validate_on_submit():
        return redirect(url_for('football.team_results', query=form.search_query.data))

    if form2.validate_on_submit():
        return redirect(url_for('football.player_results', fname=form2.fname.data, lname=form2.lname.data))

    return render_template('index.html', form = form, form2 = form2)

@main.route("/about")
def about():
    return render_template("about.html", title="About")

@main.route("/howitworks")
def how_it_works():
    return render_template("how_it_works.html", title="How It Works")

@main.route('/user/<username>')
def user_detail(username):
    # Create list of reviews done by the specified user
    reviews = Review.objects(commenter=User.objects(username=username).first())
    return render_template('user_detail.html', username = username, reviews = reviews)
