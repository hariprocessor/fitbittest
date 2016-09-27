import database as db
import fitbit
import time
import datetime
import variables as v

def get_yesterday():
	yesterday = datetime.date.fromtimestamp(time.time() - 60*60*24)
	return yesterday#.strftime('%Y-%m-%d')

def user_login(access_token, refresh_token):
	user = fitbit.Fitbit(v.CLIENT_ID, v.CLIENT_SECRET, access_token=access_token, refresh_token=refresh_token)
	return user

def get_step(user):
	yesterday=get_yesterday()
	data = user.intraday_time_series('activities/steps', base_date=yesterday.strftime('%Y-%m-%d'), detail_level='1min')
	result = list()
	for mindata in data['activities-steps-intraday']['dataset']:
		temp = dict()
		steps = int(str(mindata['value']))
		_time = str(mindata['time'])
		hour = int(_time.split(':')[0])
		minute = int(_time.split(':')[1])
		second = int(_time.split(':')[2])
		timestamp = time.mktime((yesterday.year, yesterday.month, yesterday.day, hour, minute, second, 0, 0, 0))
		temp['value'] = steps
		temp['timestamp'] = timestamp
		result.append(temp)
	return result

def main():
	for db_user in db.select_user():
		user = user_login(db_user['access_token'], db_user['refresh_token'])
		for steps in get_step(user):
			print db_user['user_id']
			print steps['timestamp']
			print steps['value']
			db.insert_fitbit(user_id=db_user['user_id'], timestamp=steps['timestamp'], step=steps['value'])

main()
