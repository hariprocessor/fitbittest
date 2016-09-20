import cherrypy
from peewee import *
import datetime
import variables as v

db = MySQLDatabase(v.DATABASE,host=v.HOST,port=3306, user=v.USER, passwd=v.PASSWD)

class GPS(Model):
	user_id = TextField()
	latitude = TextField()
	longitude = TextField()
	timestamp = TimestampField()
	class Meta:
		database = db

class User(Model):
	access_token = TextField()
	expires_in = IntegerField()
	refresh_token = TextField()
	scope = TextField()
	token_type = TextField()
	user_id = TextField()
	key = TextField()
	class Meta:
		database = db

class Fitbit(Model):
	user_id = TextField()
	timestamp = TimestampField()
	step = IntegerField()
	class Meta:
		database = db


db.connect()
#db.drop_table(GPS)
if GPS.table_exists():
	db.drop_table(GPS)
if User.table_exists():
	db.drop_table(User)
if Fitbit.table_exists():
	db.drop_table(Fitbit)

db.create_table(GPS, safe=True)
db.create_table(User, safe=True)
db.create_table(Fitbit, safe=True)
#GPS.get_create_table(fail_silently=True)

def insert_gps(user_id=None, key=None, latitude, longitude, timestamp):
	try:
		if user_id is None and key is None:
			return {'success':False}
		if key is not None:
			user_id = select_user(key=key)['user_id']
		gps = GPS(user_id=user_id, latitude=latitude, longitude=longitude, timestamp=timestamp)
		gps.save()
		return {'success':True}
	except Exception, e:
		return {'success':False, 'error_type':e}

def insert_user(access_token, expires_in, refresh_token, scope, token_type, user_id, key):
	try:
		# insert new user
		if select_user(user_id=user_id).get('key') is None:
			user = User(access_token=access_token, expires_in=expires_in, refresh_token=refresh_token, scope=scope, token_type=token_type, user_id=user_id, key=key)
			user.save()
		# update user
		else:
			User.update(access_token=access_token, expires_in=expires_in, refresh_token=refresh_token, scope=scope, token_type=token_type, key=key).where(user_id=user_id)
		return {'success':True}
	except Exception, e:
		return {'success':False, 'error_type':e}

def insert_fitbit(user_id=None, key=None, timestamp, step):
	try:
		if user_id is None and key is None:
			return {'success':False}
		if key is not None:
			user_id = select_user(key=key)['user_id']
		fitbit = Fitbit(user_id=user_id, timestamp=timestamp, step=step)
		fitbit.save()
		return {'success':True}
	except Exception, e:
		return {'success':False, 'error_type':e}

def select_gps_fitbit(user_id=None, key=None, start_timestamp, end_timestamp):
	try:
		if user_id is None and key is None:
			return {'success':False}
		if key is not None:
			user_id = select_user(key=key)['user_id']
		result = dict()
		result['user_id'] = user_id
		result['data'] = list()
		for data in GPS.select().join(Fitbit).where(Fitbit.user_id==GPS.user_id, Fitbit.timestamp==GPS.timestamp):
			temp = dict()
			temp['timestamp'] = data.timestamp
			temp['latitude'] = data.latitude
			temp['longitude'] = data.longitude
			temp['step'] = data.step
			result['data'].append(temp)
		result['success'] = True
		return result
	except Exception, e:
		return {'success':False, 'error_type':e}

def select_user(user_id=None, key=None):
	try:
		if user_id is None and key is None:
			return {'success':False}
		# select by user_id
		result = dict()
		if user_id is not None:
			for user in User.select().where(user_id==user_id):
				result['user_id'] = user.user_id
				result['access_token'] = user.access_token
				result['expires_in'] = user.expires_in
				result['refresh_token'] = user.refresh_token
				result['scope'] = user.scope
				result['token_type'] = user.token_type
				result['key'] = user.key
		else:
			for user in User.select().where(key==key):
				result['user_id'] = user.user_id
				result['access_token'] = user.access_token
				result['expires_in'] = user.expires_in
				result['refresh_token'] = user.refresh_token
				result['scope'] = user.scope
				result['token_type'] = user.token_type
				result['key'] = user.key
		result['success'] = True
		return result
	except Exception, e:
		return {'success':False, 'error_type':e}
