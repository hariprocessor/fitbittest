import cherrypy
import simplejson as json
import time
import database
import datetime
import string
import random
import hmac
import urllib2
import urllib

class fitbit(object):
	@cherrypy.expose
	def index(self):
		return "HELLO WORLD!<br>CONTACT : hariprocessor at gmail dot com"
	@cherrypy.expose
	def gps(self):
		try:
			cl = cherrypy.request.headers['Content-Length']
			rawbody = cherrypy.request.body.read(int(cl))
			body = json.loads(rawbody)
			key = body[0]['key']
			for i in range(len(body[1])):
				latitude = float(body[1][i]['latitude'])
				longitude = float(body[1][i]['longitude'])
				timestamp = body[1][i]['timestamp']
				db.insert_gps(key=key, latitude=latitude, longitude=longitude, timestamp=timestamp)
			return json.dumps({'success':'true'})
		except Exception, e:
			return json.dumps({'success':'false'})

	@cherrypy.expose
	def login(self, access_token, expires_in, refresh_token, scope, token_type, user_id):
		timestamp = int(time.time())
		key = hmac.new(user_id+str(timestamp)).hexdigest()
		result = database.insert_user(access_token, expires_in, refresh_token, scope, token_type, user_id, key)
		if result['success'] is True:
			return json.dumps({'success':'true', 'key':key})
		else:
			return json.dumps({'success':'false'})

	@cherrypy.expose
	def callback(self, code):
		return json.dumps({'success':'true', 'code':code})

if __name__ == '__main__':
	cherrypy.config.update({'server.socket_host':'0.0.0.0',
		'server.socket_port':8080,
		})
	cherrypy.quickstart(fitbit())
