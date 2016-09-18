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
		for i in range(len(body)):
			latitude = float(body[i]['latitude'])
			longitude = float(body[i]['longitude'])
			timestamp = body[i]['timestamp']
			db.insert_gps_data(cherrypy.session['user_id'], latitude, longitude, timestamp)
		return rawbody

	@cherrypy.expose
	def login(self, scopes, user_id, time_to_live, token):
		#raise cherrypy.HTTPRedirect('https://www.fitbit.com/oauth2/authorize?response_type=token&client_id=227ZFL&redirect_uri=http%3A%2F%2Flocalhost%3A8080%2Fcallback&scope=activity%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight&expires_in=604800')
		# scope
		# user id
		# time to live
		# token
		# key - timestamp + user id
		timestamp = int(time.time())
		key = hmac.new(user_id+str(timestamp))
		User.get_or_create(name=user_id)
		User.update(scope=scope, ttl=int(time_to_live), token=token, key=key).where(name=user_id)
		return key

	@cherrypy.expose
	def callback(self, code):
		#return 'MjI3WkZMOmQyZDI3NjBmZWZiOTU0ZGVjZTZhNDI3OTk1OTRiYjYw'
		return code

if __name__ == '__main__':

	cherrypy.config.update({'server.socket_host':'127.0.0.1',
		'server.socket_port':8080,
		})
	cherrypy.quickstart(fitbit())
