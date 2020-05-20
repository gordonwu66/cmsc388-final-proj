from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    email = db.EmailField(unique=True, required=True)
    username = db.StringField(unique=True, required=True)
    password = db.StringField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

# Repurpose for fantasy football player reviews (not movies)
class Review(db.Document):

	commenter = db.ReferenceField(User)
	content = db.StringField(min_length=1, max_length=500, required=True)
    draftRound=db.IntegerField(required=True)
    playAgain=db.StringField(required=True, min_length=2, max_length=3)
    date = db.StringField(required = True)
	player_name = db.StringField(required = True)
	player_id = db.StringField(min_length=7, max_length=7, regex=r'/^[A-Z]{2}-\d{4}$/', required=True)

