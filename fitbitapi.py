import fitbit

CLIENT_ID = '227ZFL'
CLIENT_SECRET = '2fc5d3d02f9fc9e5642fb4abc322a7e2'

def user_login(access_token, refresh_token):
	user = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, access_token=access_token, refresh_token=refresh_token)

def step(access_token, refresh_token):
	user_login(access_token, refresh_token)
	data = intraday_time_series('activities/steps', base_date='today', detail_level='1min')
