from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import RegistrationForm, CreateClient
from app.models import User, Client, ClientRelationship,\
					   Relationship, ClientContact,\
					   ContactType, ClientAddress,\
					   Gender, Ethnicity, Race, ClientRace

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', title = 'Home')


@app.route('/register', methods = ['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username = form.username.data, email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Now Registered')
		return redirect(url_for('login'))
	return render_template('register.html', title = 'Register', form = form)


@app.route('/create_client', methods = ['GET','POST'])
def create_client():
	race_choices = [(r.id, r.race) for r in Race.query.all()]
	ethn_choices = [(e.id, e.ethnicity) for e in Ethnicity.query.all()]
	gender_choices = [(g.id, g.gender) for g in Gender.query.all()]
	form = CreateClient()
	form.race.choices = race_choices
	form.ethnicity.choices = ethn_choices
	form.gender.choices = gender_choices
	if form.validate_on_submit():
		# Add the client to the Client table
		client = Client(first_name = form.first_name,
						middle_name = form.middle_name,
						last_name = form.last_name,
						SSN = form.SSN,
						veteran = form.veteran,
						activeMilitary = form.activeMil,
						foreignBorn = form.foreignBorn,
						race = form.race,
						ethnicity = form.ethnicity,
						gender = form.gender)
		db.session.add(client)
		db.session.commit()
	return render_template('add_client.html', title = 'Add Client', form = form)