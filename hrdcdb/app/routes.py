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
	form = CreateClient()
	if form.validate_on_submit():
		form.execute_transaction()
	return render_template('add_client.html', title = 'Add Client', form = form)


@app.route('/<form>_form', methods = ['GET', 'POST'])
def render_form(form):
	form_class = globals()[form]
	instance = form_class()
	if instance.validate_on_submit():
		instance.execute_transaction()
		return redirect(url_for('render_form', form = form))
	return render_template('form_view.html', title = instance.form_title, form = instance)