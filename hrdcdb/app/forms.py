from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, FieldList, FormField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Optional
from app.models import User

class LoginForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired()])
	password = PasswordField('Password', validators = [DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
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


# These forms will need to be altered to match whatever schema I land on for the Client table.

class CreateClient(FlaskForm):
	first_name = StringField('First Name')
	middle_name = StringField('Middle Name')
	last_name = StringField('Last Name')
	SSN = StringField('Social Security #')
	veteran = BooleanField('Veteran')
	activeMil = BooleanField('Active Military')
	disability = BooleanField('Disability')
	foreignBorn = BooleanField('Foreign Born')
	race = SelectField('Race', coerce = int, validators=[DataRequired()])
	ethnicity = SelectField('Ethnicity', coerce = int, validators=[DataRequired()])
	gender = SelectField('Gender', coerce = int, validators=[DataRequired()])
	submit = SubmitField('Add Client')



# class FilterClients(FlaskForm):
# 	gender_list_choices = list(zip(lists.genders.keys(), lists.genders.values()))
# 	race_choices = list(zip(lists.race.keys(), lists.race.values()))
# 	military_status = list(zip(lists.military.keys(), lists.military.values()))

# 	name = StringField('Name')
# 	gender = SelectField('Gender', choices = gender_list_choices, validators = [Optional()], coerce = int)
# 	race = SelectField('Race', choices = race_choices, validators = [Optional()], coerce = int)
# 	military = SelectField('Military', choices = military_status, validators = [Optional()], coerce = int)
# 	submit = SubmitField('Filter Results')