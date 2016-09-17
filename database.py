import cherrypy
from peewee import *
import datetime

db = MySQLDatabase('fitbit',host='localhost',port=3306, user='root', passwd='apmsetup')

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
    email = TextField()

db.connect()
#db.drop_table(GPS)
db.create_table(GPS, safe=True)
#GPS.get_create_table(fail_silently=True)


def insert_gps_data(user_id, latitude, longitude, timestamp):
	timestamp_ = datetime.datetime.fromtimestamp(int(timestamp))
	gps = GPS(user_id=user_id, latitude=latitude, longitude=longitude, timestamp=timestamp_)
	gps.save()
