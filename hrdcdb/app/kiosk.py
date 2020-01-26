import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from app import app, db
from app.models import *

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/work/client_secret.json', scope)
client = gspread.authorize(creds)

# sheet = client.open_by_key('1Yo4ibOuL5mFcHOuYrJ-tEuEI93HuS5zGptua_sakugs')

def read_checkin_roster():
	sheet = client.open_by_key('1Yo4ibOuL5mFcHOuYrJ-tEuEI93HuS5zGptua_sakugs')
	ws = sheet.get_worksheet(0)
	data = ws.get_all_values()
	headers = data.pop(0)

	roster = pd.DataFrame(data, columns = headers)
	return roster

def checkin_to_db():
	sheet = client.open_by_key('1Yo4ibOuL5mFcHOuYrJ-tEuEI93HuS5zGptua_sakugs')
	ws = sheet.get_worksheet(0)

	while len(ws.row_values(2)) > 0:
		data = ws.row_values(2)
		chk = Kiosk(timestamp = datetime.strptime(data[0],'%m/%d/%Y %H:%M:%S'), first_name = data[1],
		            middle_name = data[2], last_name = data[3],
		            dob = datetime.strptime(data[4], '%m/%d/%Y'), SSN = data[5])
		db.session.add(chk)
		db.session.commit()
		ws.delete_row(2)



