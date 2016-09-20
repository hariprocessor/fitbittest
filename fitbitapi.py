import fitbit
import variables as v

def user_login(access_token, refresh_token):
	user = fitbit.Fitbit(v.CLIENT_ID, v.CLIENT_SECRET, access_token=access_token, refresh_token=refresh_token)

def step(access_token, refresh_token):
	user_login(access_token, refresh_token)
	data = intraday_time_series('activities/steps', base_date='today', detail_level='1min')
