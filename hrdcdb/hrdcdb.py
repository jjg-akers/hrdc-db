from app import app, db
from app.models import User, Client, ClientRelationship,\
					   Relationship, ClientContact,\
					   ContactType, ClientAddress,\
					   Gender, Ethnicity, Race, ClientRace

@app.shell_context_processor
def make_shell_context():
	return {'db':db,
			'User':User, 
			'Client':Client,
			'ClientRelationship': ClientRelationship,
			'Relationship': Relationship,
			'ClientContact': ClientContact,
			'ContactType': ContactType,
			'ClientAddress': ClientAddress,
			'Gender': Gender,
			'Ethnicity': Ethnicity,
			'Race': Race,
			'ClientRace': ClientRace}