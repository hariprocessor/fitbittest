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
import authorization as auth
from mako.template import Template

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
			key = body['key']
			for i in range(len(body['data'])):
				latitude = float(body['data'][i]['latitude'])
				longitude = float(body['data'][i]['longitude'])
				timestamp = float(body['data'][i]['timestamp'])
				success = db.insert_gps(key=key, latitude=latitude, longitude=longitude, timestamp=timestamp)
				print success
				if not success['success']:
					print success['error_type']
					return json.dumps({'success':'false'})
			return json.dumps({'success':'true'})
		except Exception, e:
			print e
			return json.dumps({'success':'false'})

	# @cherrypy.expose
	# def login(self, access_token, expires_in, refresh_token, scope, token_type, user_id):
	# 	timestamp = int(time.time())
	# 	key = hmac.new(str(user_id)+str(timestamp)).hexdigest()
	# 	result = db.insert_user(access_token, expires_in, refresh_token, scope, token_type, user_id, key)
	# 	if result['success'] is True:
	# 		return json.dumps({'success':'true', 'key':key})
	# 	else:
	# 		return json.dumps({'success':'false'})

	@cherrypy.expose
	def callback(self, code):
		print 'callback'+'*****************************'
		response = auth.get_token(code)
		if not response['success']:
			return json.dumps({'success':'false'})
		key = auth.make_key(response['user_id'])
		insert_user = db.insert_user(response['access_token'], response['expires_in'], response['refresh_token'], response['scope'], response['token_type'], response['user_id'], key)
		if insert_user['success']:
			exists = insert_user['exists']
		result = {'success':'true', 'key':key}
		if exists:
			result['exists'] = 'true'
		else:
			result['exists'] = 'false'
		return json.dumps(result)

	@cherrypy.expose
	def logout(self, key):
		select_user = db.select_user(key=key)
		if not select_user['success']:
			return json.dumps({'success':'false', 'error_type':select_user['error_type']})
		delete_user_info = db.delete_user_info(key=key)
		if not delete_user_info['success']:
			return json.dumps({'success':'false', 'error_type':delete_user_info['error_type']})
		return json.dumps({'success':'true'})

	@cherrypy.expose
	def gpstest(self):
		cl = cherrypy.request.headers['Content-Length']
		rawbody = cherrypy.request.body.read(int(cl))

		print "******************"
		body = json.loads(rawbody)
		if 'wifi' in body:
			print "******************"
			print "wifi"
			for data in body['wifi']:
				bssid = data['bssid']
				ssid = data['ssid']
				level = data['level']
				timestamp = float(data['timestamp'])
				db.insert_wifi(user_id='1', bssid=bssid, ssid=ssid, level=level, timestamp=timestamp)
		if 'gps' in body:
			print "******************"
			print 'GPS'
			for data in body['gps']:
				latitude = float(data['latitude'])
				longitude = float(data['longitude'])
				timestamp = float(data['timestamp'])
				db.insert_gps(user_id='1', latitude=latitude, longitude=longitude, timestamp=timestamp)
		if 'step' in body:
			print "******************"
			print "step"
			for data in body['step']:
				step = int(data['step'])
				timestamp = float(data['timestamp'])
				db.insert_step(user_id='1', step_count=step, timestamp=timestamp)

	@cherrypy.expose
	def gpsresult(self):
		gps_html = """
			<table>
				<tr>
					<th>timestamp</th>
					<th>latitude</th>
					<th>longitude</th>
				</tr>
				for i in range()
				<tr>
					<td></td>
					<td></td>
					<td></td>
				</tr>

			</table>
		"""

	@cherrypy.expose
	def wifiresult(self):
		wifi_html = """
			<table>
				<tr>

				</tr>
			</table>
		"""

def timestampConvert(timestamp):
	return datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
	cherrypy.config.update({'server.socket_host':'0.0.0.0',
		'server.socket_port':8080,
		})
	cherrypy.quickstart(fitbit())
