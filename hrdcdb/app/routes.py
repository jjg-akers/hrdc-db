from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import *
from app.models import *


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


@app.route('/find_clients', methods = ['GET', 'POST'])
def view_clients():
	form = FilterClients()
	if form.validate_on_submit():
		clients = Client.query
		if form.first_name.data:
			clients = clients.filter(Client.first_name.like('%{}%'.format(form.first_name.data)))
		if form.last_name.data:
			clients = clients.filter(Client.last_name.like('%{}%'.format(form.last_name.data)))
		return render_template('search_results.html', title = 'Search Results', form = form, clients = clients)
	return render_template('search_results.html', title = 'Client Search', form = form)


@app.route('/client_<clientid>_dashboard')
def client_dashboard(clientid):
	client = Client.query.filter(Client.id == clientid).first()
	a = ClientRelationship.query.filter(ClientRelationship.client_a_id == clientid).all()
	b = ClientRelationship.query.filter(ClientRelationship.client_b_id == clientid).all()
	relations = list(set().union(a,b))

	contact_info = ClientContact.query.filter(ClientContact.client_id == clientid).all()
	return render_template('client_dashboard.html', 
							title = '{} {} Dashboard'.format(client.first_name, client.last_name),
							client = client, relations = relations, contact_info = contact_info)


@app.route('/client_<clientid>_contact', methods = ['GET', 'POST'])
def create_contact(clientid):
	form = CreateClientContact()
	contact_info = ClientContact.query.filter(ClientContact.client_id == clientid).all()
	if form.validate_on_submit():
		new_contact = ClientContact(client_id = clientid,
									contact = form.contact_info.data,
									contact_type = form.contact_type.data)
		db.session.add(new_contact)
		db.session.commit()
		return redirect(url_for('create_contact', clientid = clientid))
	return render_template('create_contact.html', title = 'Create Contact', form = form, contact_info = contact_info)


@app.route('/create_relationship_<clientid>', defaults = {'second_client':None}, methods = ['GET','POST'])
@app.route('/create_relationship_<clientid>_<second_client>', methods = ['GET','POST'])
def create_relationship(clientid, second_client):
	form = CreateRelationship()
	a = ClientRelationship.query.filter(ClientRelationship.client_a_id == clientid).all()
	b = ClientRelationship.query.filter(ClientRelationship.client_b_id == clientid).all()
	rels = list(set().union(a,b))
	if form.validate_on_submit():
		rel = ClientRelationship(client_a_id = form.first_client.data,
								 client_b_id = form.second_client.data,
								 a_to_b_relation = form.relationship.data)
		db.session.add(rel)
		db.session.commit()
		return redirect(url_for('create_relationship', clientid = clientid))
	return render_template('create_relationship.html', title = 'Create Relationship', data = rels, form = form)	


@app.route('/edit_client_<clientid>', methods = ['GET','POST'])
def edit_client(clientid):
	client = Client.query.filter(Client.id == clientid).first()
	data = client.__dict__
	del data['_sa_instance_state']
	data['activeMil'] = data['activeMilitary']
	del data['activeMilitary']
	form = EditClient(data = data)

	return render_template('form_view.html', form = form)