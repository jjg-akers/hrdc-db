from app import app, db
from app.models import User, Client, ClientRelationship,\
					   Relationship, ClientContact,\
					   ContactType, ClientAddress,\
					   Gender, Ethnicity, Race, ClientRace


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


Ethnicity.query.delete()
Race.query.delete()
Gender.query.delete()
ContactType.query.delete()
Relationship.query.delete()

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

db.session.commit()