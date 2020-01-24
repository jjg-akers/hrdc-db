from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_user, logout_user, login_required
from app import app, db
from app.forms import *
from app.models import *
from app.kiosk import read_checkin_roster


# This line is put in to test branch switching
# It should only appear in the serv branch

@app.route('/login', methods = ['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username = form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user, remember = form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/index')
@login_required
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
	return render_template('form_view.html', title = 'Register', form = form)


@app.route('/create_client', methods = ['GET','POST'])
@login_required
def create_client():
	form = CreateClient()
	if form.validate_on_submit():
		client = Client(first_name = form.first_name.data,
						middle_name = form.middle_name.data,
						last_name = form.last_name.data,
						dob = form.dob.data,
						SSN = form.SSN.data,
						veteran = form.veteran.data,
						activeMilitary = form.activeMilitary.data,
						disability = form.disability.data,
						foreignBorn = form.foreignBorn.data,
						ethnicity = form.ethnicity.data,
						gender = form.gender.data,
						created_by = current_user.id)
		db.session.add(client)
		db.session.commit()
		clientRace = ClientRace(client_id = client.id, race_id = form.race.data, created_by = current_user.id)
		db.session.add(clientRace)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('form_view.html', title = 'Add Client', form = form)


@app.route('/<form>_form', methods = ['GET', 'POST'])
@login_required
def render_form(form):
	form_class = globals()[form]
	instance = form_class()
	if instance.validate_on_submit():
		instance.execute_transaction()
		return redirect(url_for('render_form', form = form))
	return render_template('form_view.html', title = instance.form_title, form = instance)


@app.route('/find_clients', methods = ['GET', 'POST'])
@login_required
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
@login_required
def client_dashboard(clientid):
	client = Client.query.filter(Client.id == clientid).first()
	relations = ClientRelationship.query.filter(ClientRelationship.client_a_id == clientid).all()

	contact_info = ClientContact.query.filter(ClientContact.client_id == clientid).all()
	return render_template('client_dashboard.html', 
							title = '{} {} Dashboard'.format(client.first_name, client.last_name),
							client = client, relations = relations, contact_info = contact_info)


@app.route('/client_<clientid>_contact', methods = ['GET', 'POST'])
@login_required
def create_contact(clientid):
	form = CreateClientContact()
	contact_info = ClientContact.query.filter(ClientContact.client_id == clientid).all()
	if form.validate_on_submit():
		new_contact = ClientContact(client_id = clientid,
									contact = form.contact_info.data,
									contact_type = form.contact_type.data,
									created_by = current_user.id)
		db.session.add(new_contact)
		db.session.commit()
		return redirect(url_for('create_contact', clientid = clientid))
	return render_template('create_contact.html', title = 'Create Contact', form = form, contact_info = contact_info)


@app.route('/create_relationship_<clientid>', defaults = {'second_client':None}, methods = ['GET','POST'])
@app.route('/create_relationship_<clientid>_<second_client>', methods = ['GET','POST'])
@login_required
def create_relationship(clientid, second_client):
	form = CreateRelationship()
	rels = ClientRelationship.query.filter(ClientRelationship.client_a_id == clientid).all()
	if form.validate_on_submit():
		rel = ClientRelationship(client_a_id = form.first_client.data,
								 client_b_id = form.second_client.data,
								 a_to_b_relation = form.relationship.data,
								 created_by = current_user.id)
		if form.relationship.data in [1,6,7,8,9]:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = form.relationship.data,
								 		  created_by = current_user.id)
		elif form.relationship.data == 2:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = 5,
								 		  created_by = current_user.id)
		elif form.relationship.data == 5:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = 2,
								 		  created_by = current_user.id)
		elif form.relationship.data == 3:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = 4,
								 		  created_by = current_user.id)
		elif form.relationship.data == 4:
			back_rel = ClientRelationship(client_a_id = form.second_client.data,
								 		  client_b_id = form.first_client.data,
								 		  a_to_b_relation = 3,
								 		  created_by = current_user.id)
		db.session.add(rel)
		db.session.add(back_rel)
		db.session.commit()
		return redirect(url_for('create_relationship', clientid = clientid))
	return render_template('create_relationship.html', title = 'Create Relationship', data = rels, form = form)	


@app.route('/edit_client_<clientid>', methods = ['GET','POST'])
@login_required
def edit_client(clientid):
	client = Client.query.filter(Client.id == clientid).first()
	form = EditClient(data = client.__dict__)
	if form.validate_on_submit():
		client.first_name = form.first_name.data
		client.middle_name = form.middle_name.data
		client.last_name = form.last_name.data
		client.dob = form.dob.data
		client.SSN = form.SSN.data
		client.veteran = form.veteran.data
		client.activeMilitary = form.activeMilitary.data
		client.gender = form.gender.data
		client.ethnicity = form.ethnicity.data
		db.session.commit()
	return render_template('form_view.html', form = form)


# record_type is the name of the model as a string
# e.g. 'Program'
@app.route('/add_<record_type>', methods = ['GET','POST'])
def add_record(record_type):
	record_class = globals()[record_type]
	record_form = globals()['Create'+record_type]
	instance = record_form()
	records = record_class.query.all()
	if instance.validate_on_submit():
		instance.execute_transaction()
		return redirect(url_for('add_record', record_type = record_type))
	return render_template('add_record.html', title = instance.form_title, form = instance, data = records)


@app.route('/add_Service_<clientid>', methods = ['GET','POST'])
def add_service(clientid):
	services = Service.query.filter(Service.client_id == clientid).all()
	form = CreateService()
	if form.validate_on_submit():
		new_service = Service(service_type_id = form.service_type.data,
							  client_id = clientid,
							  program_id = form.program.data,
							  created_by = current_user.id,
							  begin_date = form.begin_date.data,
							  end_date = form.end_date.data)
		db.session.add(new_service)
		db.session.commit()
		return redirect(url_for('add_service', clientid = clientid))
	return render_template('add_service.html', title = 'Add Service', form = form, data = services)


@app.route('/client_checkin', methods = ['GET','POST'])
def client_checkin():
	roster = read_checkin_roster()
	return render_template('client_checkin.html', roster = roster)