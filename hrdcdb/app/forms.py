from flask import redirect, url_for
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional, Regexp
from app.models import *
from app import db


class LoginForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	form_title = 'Create New User'

	username = StringField('Username', validators = [DataRequired()])
	email = StringField('Email', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	password2 = PasswordField(
		'Repeat Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username = username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def validate_email(self, email):
		user = User.query.filter_by(email = email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address.')

	def execute_transaction(self):
		user = User(username = self.username.data, email = self.email.data)
		user.set_password(self.password.data)
		db.session.add(user)
		db.session.commit()


class CreateClient(FlaskForm):
	form_title = 'Create New Client'

	first_name = StringField('First Name', validators=[DataRequired()])
	middle_name = StringField('Middle Name')
	last_name = StringField('Last Name', validators=[DataRequired()])

	dob = DateField('Date of Birth', format='%Y-%m-%d')
	ssn_regex = '^(?!(000|666|9))\\d{3}-(?!00)\\d{2}-(?!0000)\\d{4}$'
	SSN = StringField('Social Security #', validators = [Optional(), Regexp(ssn_regex, message = 'Invalid Social Security Number')])
	veteran = BooleanField('Veteran')
	activeMilitary = BooleanField('Active Military')
	disability = BooleanField('Disability')
	foreignBorn = BooleanField('Foreign Born')

	race_choices = [(r.id, r.race) for r in Race.query.all()]
	ethn_choices = [(e.id, e.ethnicity) for e in Ethnicity.query.all()]
	gender_choices = [(g.id, g.gender) for g in Gender.query.all()]
	race = SelectField('Race', choices = race_choices, coerce = int, validators=[DataRequired()])
	ethnicity = SelectField('Ethnicity', choices = ethn_choices, coerce = int, validators=[DataRequired()])
	gender = SelectField('Gender', choices = gender_choices, coerce = int, validators=[DataRequired()])


	submit = SubmitField('Add Client')

	def validate_SSN(self, SSN):
		client = Client.query.filter_by(SSN = SSN.data).first()
		if client is not None:
			raise ValidationError('A client already exists with that SSN')


class EditClient(FlaskForm):
	form_title = 'Edit Client'

	first_name = StringField('First Name', validators=[DataRequired()])
	middle_name = StringField('Middle Name')
	last_name = StringField('Last Name', validators=[DataRequired()])
	dob = DateField('Date of Birth', format='%Y-%m-%d')

	ssn_regex = '^(?!(000|666|9))\\d{3}-(?!00)\\d{2}-(?!0000)\\d{4}$'
	SSN = StringField('Social Security #', validators = [Regexp(ssn_regex, message = 'Invalid Social Security Number')])
	veteran = BooleanField('Veteran')
	activeMilitary = BooleanField('Active Military')
	disability = BooleanField('Disability')
	foreignBorn = BooleanField('Foreign Born')

	race_choices = [(r.id, r.race) for r in Race.query.all()]
	ethn_choices = [(e.id, e.ethnicity) for e in Ethnicity.query.all()]
	gender_choices = [(g.id, g.gender) for g in Gender.query.all()]
	race = SelectField('Race', choices = race_choices, coerce = int, validators=[DataRequired()])
	ethnicity = SelectField('Ethnicity', choices = ethn_choices, coerce = int, validators=[DataRequired()])
	gender = SelectField('Gender', choices = gender_choices, coerce = int, validators=[DataRequired()])


	submit = SubmitField('Save Changes')


class FilterClients(FlaskForm):
	form_title = 'Search For Client'

	first_name = StringField('First Name')
	middle_name = StringField('Middle Name')
	last_name = StringField('Last Name')
	dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[Optional()])
	SSN = StringField('Social Security #')

	exact_match = BooleanField('Require Exact Match')
	submit = SubmitField('Find Client')


class CreateClientContact(FlaskForm):
	form_title = 'Add Contact Information'

	contact_info = StringField('Contact Information', validators = [DataRequired()])
	contact_choices = [(c.id, c.contact_type) for c in ContactType.query.all()]
	contact_type = SelectField('Contact Type', coerce = int, choices = contact_choices, validators = [DataRequired()])

	submit = SubmitField('Add Contact Information')

	def execute_transaction(clientid):
		new_contact = ClientContact(client_id = clientid,
									contact = self.contact_info.data,
									contact_type = self.contact_type.data)
		db.session.add(new_contact)
		db.session.commit()


class CreateRelationship(FlaskForm):
	form_title = 'Create Relationship'

	client_choices = [(c.id, str(c.first_name)+' '+str(c.last_name)) for c in Client.query.all()]
	rel_choices = [(r.id, r.relationship) for r in Relationship.query.all()]

	first_client = SelectField('First Client', choices = client_choices, coerce = int, validators=[DataRequired()])
	second_client = SelectField('Second Client', choices = client_choices, coerce = int, validators=[DataRequired()])
	relationship = SelectField('Relationship', choices = rel_choices, coerce = int, validators = [DataRequired()])

	def validate(self):
		if not FlaskForm.validate(self):
			return False
		if self.first_client.data == self.second_client.data:
			self.second_client.errors.append('Must be two different clients')
			return False
		else:
			return True

	submit = SubmitField('Add Relationship')


class CreateServiceType(FlaskForm):
	form_title = 'Create Service Type'

	name = StringField('Service Type Name', validators=[DataRequired()])
	submit = SubmitField('Add Service Type')

	def validate_name(self, name):
		service_type = ServiceType.query.filter_by(name = name.data).first()
		if service_type is not None:
			raise ValidationError('A service type by that name already exists.')

	def execute_transaction(self):
		new_service_type = ServiceType(name = self.name.data)
		db.session.add(new_service_type)
		db.session.commit()


class CreateProgram(FlaskForm):
	form_title = 'Create Program'

	name = StringField('Program Name', validators = [DataRequired()])
	submit = SubmitField('Add Service Type')

	def validate_username(self, name):
		program = Program.query.filter_by(name = name.data).first()
		if program is not None:
			raise ValidationError('A program by that name already exists.')

	def execute_transaction(self):
		new_program = Program(name = self.name.data)
		db.session.add(new_program)
		db.session.commit()


class CreateService(FlaskForm):
	form_title = 'Create Program'

	program_choices = [(p.id, p.name) for p in Program.query.all()]
	ServiceType_choices = [(st.id, st.name) for st in ServiceType.query.all()]

	program = SelectField('Program', choices = program_choices, coerce = int)
	service_type = SelectField('Service Type', choices = ServiceType_choices, coerce = int)
	begin_date = DateField('Begin Date', format='%Y-%m-%d')
	end_date = DateField('End Date', format='%Y-%m-%d')
	submit = SubmitField('Add Service')