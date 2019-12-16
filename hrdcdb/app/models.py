from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
	return User.query.get(int(id))


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index = True, unique = True)
	email = db.Column(db.String(120), index = True, unique = True)
	password_hash = db.Column(db.String(128))

	def __repr__(self):
		return '<User {}>'.format(self.username)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)


class Client(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.String(20))
	middle_name = db.Column(db.String(20))
	last_name = db.Column(db.String(20))
	SSN = db.Column(db.String(11))
	veteran = db.Column(db.Boolean)
	activeMilitary = db.Column(db.Boolean)
	foreignBorn = db.Column(db.ForeignBorn)
	race = db.relationship('ClientRace', backref = 'Client Race', lazy = 'dynamic')
	ethnicity = db.Column(db.Integer, db.ForeignKey('ethnicity.id'))

class Ethnicity(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	ethnicity = db.Column(db.String(30))


class Race(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	race = db.Column(db.String(40))


class ClientRace(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
