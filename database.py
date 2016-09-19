import cherrypy
from peewee import *
import datetime

db = MySQLDatabase('fitbit',host='127.0.0.1',port=3306, user='root', passwd='apmsetup')

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

def insert_gps_data(user_id, latitude, longitude, timestamp):
	timestamp_ = datetime.datetime.fromtimestamp(int(timestamp))
	gps = GPS(user_id=user_id, latitude=latitude, longitude=longitude, timestamp=timestamp_)
	gps.save()

def user_list():
	users = list()
	for user in User.select():
		users.append(dict(access_token=user.access_token, user_id=user.user_id))
	return users

def retrieve_user_id(key='null', access_token='null'):
	user_id = 'null'
	if key != 'null':
		for user in User.select().where(key==key):
			user_id = user.user_id
	elif access_token != 'null':
		for user in User.select().where(access_token==access_token):
			user_id = user.user_id
	return user_id


def retrieve_token(key):
	# select token from user where key=something
	key = list()
	for user in User.select().where(User.key==key):
		key=[user.access_token, user.refresh_token]
	return key

def insert_step_data(user_id, timestamp, step):
	timestamp_ = datetime.datetime.fromtimestamp(int(timestamp))
	fitbit = Fitbit(user_id=user_id, timestamp=timestamp_, step=step)
	fitbit.save()
