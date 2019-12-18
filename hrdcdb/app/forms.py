from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional, Regexp
from app.models import User, Race, Ethnicity, Gender, Client, ClientRace
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
		user = User(username = form.username.data, email = form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()


# These forms will need to be altered to match whatever schema I land on for the Client table.

class CreateClient(FlaskForm):
	form_title = 'Create New Client'

	first_name = StringField('First Name', validators=[DataRequired()])
	middle_name = StringField('Middle Name', validators=[DataRequired()])
	last_name = StringField('Last Name', validators=[DataRequired()])

	ssn_regex = '^(?!(000|666|9))\\d{3}-(?!00)\\d{2}-(?!0000)\\d{4}$'
	SSN = StringField('Social Security #', validators = [DataRequired(),
														 Regexp(ssn_regex, message = 'Invalid Social Security Number')])
	veteran = BooleanField('Veteran')
	activeMil = BooleanField('Active Military')
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

	def execute_transaction(self):
		client = Client(first_name = self.first_name.data,
						middle_name = self.middle_name.data,
						last_name = self.last_name.data,
						SSN = self.SSN.data,
						veteran = self.veteran.data,
						activeMilitary = self.activeMil.data,
						foreignBorn = self.foreignBorn.data,
						ethnicity = self.ethnicity.data,
						gender = self.gender.data)
		db.session.add(client)
		db.session.commit()
		clientRace = ClientRace(client_id = client.id, race_id = self.race.data)
		db.session.add(clientRace)
		db.session.commit()



# class FilterClients(FlaskForm):
# 	gender_list_choices = list(zip(lists.genders.keys(), lists.genders.values()))
# 	race_choices = list(zip(lists.race.keys(), lists.race.values()))
# 	military_status = list(zip(lists.military.keys(), lists.military.values()))

# 	name = StringField('Name')
# 	gender = SelectField('Gender', choices = gender_list_choices, validators = [Optional()], coerce = int)
# 	race = SelectField('Race', choices = race_choices, validators = [Optional()], coerce = int)
# 	military = SelectField('Military', choices = military_status, validators = [Optional()], coerce = int)
# 	submit = SubmitField('Filter Results')