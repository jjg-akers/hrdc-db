import pandas as pd
from app import app, db
from app.models import *


race_list = ['White','Another Race','Black or African American','Asian',
			 'Native Hawaiian or Pacific Islander',
			 'American Indian or Alaska Native', 'Unknown']

ethnicity_list = ['Hispanic or Latino','Not Hispanic or Latino','Unknown']

gender_list = ['Male','Female','Nonbinary','Unknown']

contact_types = ['Work','Home','Cell','Fax','Email']

relationships = ['Spouse/Partner','Parent',
				 'Grandparent','Grandchild',
				 'Child','Sibling','Friend',
				 'Other Relative', 'Other Non-Relative']

programs = ['Housing','Energy','Food Bank','Galavan']

service_types = ['Case Management','Intake','Food Box','Emergency Shelter',
				 'Energy Assistance','Weatherization','Medical Ride','Social Ride']


Ethnicity.query.delete()
Race.query.delete()
Gender.query.delete()
ContactType.query.delete()
Relationship.query.delete()
ServiceType.query.delete()
Program.query.delete()
ProgramServiceType.query.delete()
Service.query.delete()


# Uncomment this section to drop all client data
# Client.query.delete()
# ClientRelationship.query.delete()
# ClientAddress.query.delete()
# ClientContact.query.delete()
# ClientRace.query.delete()
# Kiosk.query.delete()

db.session.commit()

for r in race_list:
	cur = Race(race = r)
	db.session.add(cur)

for e in ethnicity_list:
	cur = Ethnicity(ethnicity = e)
	db.session.add(cur)

for g in gender_list:
	cur = Gender(gender = g)
	db.session.add(cur)

for c in contact_types:
	cur = ContactType(contact_type = c)
	db.session.add(cur)

for r in relationships:
	cur = Relationship(relationship = r)
	db.session.add(cur)

for s in service_types:
	cur = ServiceType(name = s)
	db.session.add(cur)

for p in programs:
	cur = Program(name = p)
	db.session.add(cur)

# zips = pd.read_csv('zip_data.csv', dtype = {'zipcode':str})
# zips['id'] = zips.index
# zips.to_sql('city_zip', con = db.engine, if_exists='append', index = False)

db.session.commit()