import cherrypy
from peewee import *
import datetime

db = MySQLDatabase('fitbit',host='127.0.0.1',port=3306, user='root', passwd='apmsetup')

class GPS(Model):
	user_id = IntegerField()
	latitude = TextField()
	longitude = TextField()
	timestamp = TimestampField()
	class Meta:
		database = db

class User(Model):
	token = TextField()
	name = TextField()
	ttl = IntegerField()
	email = TextField()
	key = TextField()scope = TextField()

db.connect()
#db.drop_table(GPS)
db.create_table(GPS, safe=True)
db.create_table(User, safe=True)
#GPS.get_create_table(fail_silently=True)

def insert_gps_data(user_id, latitude, longitude, timestamp):
	timestamp_ = datetime.datetime.fromtimestamp(int(timestamp))
	gps = GPS(user_id=user_id, latitude=latitude, longitude=longitude, timestamp=timestamp_)
	gps.save()

def retrieve_token_from_user(key):
	# select token from user where key=something
	query = User.select(access_token, refresh_token).where(User.key==key)
	