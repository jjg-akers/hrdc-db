import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('C:/work/hrdc-db/hrdcdb/app/client_secret.json', scope)
client = gspread.authorize(creds)

# sheet = client.open_by_key('1Yo4ibOuL5mFcHOuYrJ-tEuEI93HuS5zGptua_sakugs')

def read_checkin_roster():
	sheet = client.open_by_key('1Yo4ibOuL5mFcHOuYrJ-tEuEI93HuS5zGptua_sakugs')
	ws = sheet.get_worksheet(0)
	data = ws.get_all_values()
	headers = data.pop(0)

	roster = pd.DataFrame(data, columns = headers)
	return roster


