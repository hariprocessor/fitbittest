import cherrypy
import simplejson as json
import time
import database as db
import datetime
import string
import random
import hmac
import urllib2
import urllib

CLIENT_ID = '227ZFL'
CLIENT_SECRET = '2fc5d3d02f9fc9e5642fb4abc322a7e2'

class fitbit(object):
	@cherrypy.expose
	def gps(self):
		cl = cherrypy.request.headers['Content-Length']
		rawbody = cherrypy.request.body.read(int(cl))
		body = json.loads(rawbody)
		key = body[0]['key']
		for i in range(len(body[1])):
			latitude = float(body[1][i]['latitude'])
			longitude = float(body[1][i]['longitude'])
			timestamp = body[1][i]['timestamp']
			print str(latitude) + str(longitude) + timestamp
			db.insert_gps_data(key, latitude, longitude, timestamp)
		return rawbody

	@cherrypy.expose
	def login(self, access_token, expires_in, refresh_token, scope, token_type, user_id):
		timestamp = int(time.time())
		key = hmac.new(user_id+str(timestamp))
		User.get_or_create(user_id=user_id)
		User.update(access_token=access_token, expires_in=expires_in, refresh_token=refresh_token, scope=scope, token_type=token_type, key=key).where(user_id=user_id)
		return key

	@cherrypy.expose
	def callback(self, code):
		#return 'MjI3WkZMOmQyZDI3NjBmZWZiOTU0ZGVjZTZhNDI3OTk1OTRiYjYw'
		return code

	@cherrypy.expose
	def show(self):
		return 'hi'
		

if __name__ == '__main__':

	cherrypy.config.update({'server.socket_host':'127.0.0.1',
		'server.socket_port':8080,
		})
	cherrypy.quickstart(fitbit())
