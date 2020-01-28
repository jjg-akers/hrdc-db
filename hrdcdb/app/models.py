from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin


@login.user_loader
def load_user(id):
	return User.query.get(int(id))

################################################################################
# User table defines the staff that will login and do data entry and reporting #
################################################################################


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


################################################################
# The Kiosk model collects data from a customer check-in kiosk #
################################################################


class Kiosk(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	timestamp = db.Column(db.DateTime, index = True)
	first_name = db.Column(db.String(20))
	middle_name = db.Column(db.String(20))
	last_name = db.Column(db.String(20))
	dob = db.Column(db.Date)
	SSN = db.Column(db.String(4))
	seen = db.Column(db.Boolean)
	cleared = db.Column(db.Boolean)

	def __repr__(self):
		return '<{} {} check-in>'.format(self.first_name, self.timestamp)



#################################################################################
# The Client tables define demographic and family information about each client #
#################################################################################

class Client(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	first_name = db.Column(db.String(20))
	middle_name = db.Column(db.String(20))
	last_name = db.Column(db.String(20))
	SSN = db.Column(db.String(11))
	veteran = db.Column(db.Boolean)
	activeMilitary = db.Column(db.Boolean)
	disability = db.Column(db.Boolean)
	foreignBorn = db.Column(db.Boolean)
	ethnicity = db.Column(db.Integer, db.ForeignKey('ethnicity.id'))
	gender = db.Column(db.Integer, db.ForeignKey('gender.id'))
	dob = db.Column(db.Date)
	created_date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

	gen = db.relationship('Gender', uselist = False)
	race = db.relationship('ClientRace', uselist = False)
	user = db.relationship('User', uselist = False)
	eth = db.relationship('Ethnicity', uselist = False)

	def __repr__(self):
		return '<{} {}>'.format(self.first_name,self.last_name)


class ClientRelationship(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	client_a_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	client_b_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	a_to_b_relation = db.Column(db.Integer, db.ForeignKey('relationship.id'))
	relationship = db.relationship('Relationship', uselist=False)
	client_a = db.relationship('Client', foreign_keys=[client_a_id])
	client_b = db.relationship('Client', foreign_keys=[client_b_id])
	created_date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', uselist = False)


class Relationship(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	relationship = db.Column(db.String(15))

	def __repr__(self):
		return '<Relationship Type {}>'.format(self.relationship)


class ClientContact(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	contact = db.Column(db.String(50))
	contact_type = db.Column(db.Integer, db.ForeignKey('contact_type.id'))
	ContactType = db.relationship('ContactType', uselist = False)
	created_date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', uselist = False)


class ContactType(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	contact_type = db.Column(db.String(10))

	def __repr__(self):
		return '<Contact Type {}>'.format(self.contact_type)


class ClientAddress(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	address = db.Column(db.String(50))
	address_2 = db.Column(db.String(50))
	city = db.Column(db.String(30))
	state = db.Column(db.String(30))
	zipcode = db.Column(db.String(5))
	start_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	created_date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', uselist = False)



class Gender(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	gender = db.Column(db.String(10))

	def __repr__(self):
		return '<Gender {}>'.format(self.gender)


class Ethnicity(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	ethnicity = db.Column(db.String(30))

	def __repr__(self):
		return '<Ethnicity {}>'.format(self.ethnicity)


class Race(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	race = db.Column(db.String(40))

	def __repr__(self):
		return '<Race {}>'.format(self.race)


class ClientRace(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	race_id = db.Column(db.Integer, db.ForeignKey('race.id'))
	race = db.relationship('Race', uselist = False)
	created_date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
	user = db.relationship('User', uselist = False)


####################################################################################
# The Program and Service tables define how services are tracked across the agency #
####################################################################################

class ServiceType(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50))

	def __repr__(self):
		return '<ServiceType {}>'.format(self.name)


class Program(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(20))

	def __repr__(self):
		return '<Program {}>'.format(self.name)


class Service(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	service_type_id = db.Column(db.Integer, db.ForeignKey('service_type.id'))
	client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
	program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
	created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
	created_date = db.Column(db.DateTime, index = True, default = datetime.utcnow)
	begin_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)
	program = db.relationship('Program', uselist = False)
	user = db.relationship('User', uselist = False)
	service_type = db.relationship('ServiceType', uselist = False)
	client = db.relationship('Client', uselist = False)

	def __repr__(self):
		return '<Service {}>'.format(self.id)


class ProgramServiceType(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
	service_type_id = db.Column(db.Integer, db.ForeignKey('service_type.id'))
	program = db.relationship('Program', uselist = False)
	service_type = db.relationship('ServiceType', uselist = False)

	def __repr__(self):
		return '<ProgramServiceType {}>'.format(self.id)


##########################################################
# The Assessment tables track client status and outcomes #
##########################################################


# class Assessment(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	assessment_type = db.Column(db.Integer, db.ForeignKey('assessmenttype.id'))
# 	client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
# 	program_id = db.Column(db.Integer, db.ForeignKey('program.id'))
# 	user_id = db.Column(db.Integer, db.ForeignKey('client.id'))
# 	assessment_date = db.Column(db.DateTime)


# class FinancialAssessment(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	income = db.relationship('Income', backref = 'Assessment', lazy = 'dynamic')


# class IncomeType(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	income_type = db.Column(db.String(30))


# class IncomeAssessment(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	income_type_id = db.Column(db.Integer, db.ForeignKey('incometype.id'))
# 	assessment_id = db.Column(db.Integer, db.ForeignKey('assessment.id'))
# 	amount = db.Column(db.Integer)


# class HousingAssessment(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	# This will be filled in with columns that represent housing assessment questions


# class OutcomeMatrix(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	# This will be filled in with columns for each outcome matrix domain


# class NonCashBenefits(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	benefit = db.Column(db.String(20))


# class ClientNCBs(db.Model):
# 	id = db.Column(db.Integer, primary_key = True)
# 	assessment = db.Column(db.Integer, db.ForeignKey('assessment.id'))
# 	benefit_id = db.Column(db.Integer, db.ForeignKey('noncashbenefits.id'))
