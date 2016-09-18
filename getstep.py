import database
import fitbit
import time

CLIENT_ID = '227ZFL'
CLIENT_SECRET = '2fc5d3d02f9fc9e5642fb4abc322a7e2'

def get_yesterday():
	today = date.today()
	yesterday = date.fromtimestamp(time.time() - 60*60*24)
	return yesterday.strftime("%Y-%m-%d")

def user_login(access_token, refresh_token):
	user = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token=access_token, refresh_token=refresh_token)
	return user

def step(access_token, refresh_token):
	user_login(access_token, refresh_token)
	data = intraday_time_series('activities/steps', base_date=yesterday, detail_level='1min')
	for mindata in data['activities-steps-intraday']['dataset']:
		steps = str(mindata['value'])
		time = str(mindata['time'])
		mintime = time.split(':')[0]
		

for user in database.user_list():
	user_login(user.)