import fitbit
import simplejson as json

client_id = '227SVP'
client_secret = '7a0a6ec949e4add5c71204a689005aa8'
access_token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiI0V1BTQlAiLCJhdWQiOiIyMjdTVlAiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcmFjdCBybG9jIHJ3ZWkgcmhyIHJudXQgcnBybyByc2xlIiwiZXhwIjoxNDczNjE4OTQ2LCJpYXQiOjE0NzM1OTAxNDZ9.DlCqcgBHKb8VqxcuMrY8V3CBzXIABFOlMc4AqjMpS94'
refresh_token = '71fecfb23a6f7eed69c874d264d9200976bfcbf6c7feedb5340a48014e678a28'

authd_client = fitbit.Fitbit(client_id, client_secret, access_token=access_token, refresh_token=refresh_token)

# get user profile
def user_profile_get_()
	user_profile_raw = authd_client.user_profile_get()
	user_full_name = user_profile_raw['user']['fullName']
	return user_full_name.encode()

