import cherrypy
import simplejson as json
import time
import database as db
import datetime
import string
import random
from fitbit.api import FitbitOauth2Client

class fitbit(object):
	# def __init__(self,
	# 			redirect_uri='http://127.0.0.1:8080/'):
	# 	""" Initialize the FitbitOauth2Client """
	# 	self.redirect_uri = redirect_uri
	# 	self.oauth = FitbitOauth2Client(client_id, client_secret)
	# 	self.success_html = """
	# 		<h1>You are now authorized to access the Fitbit API!</h1>
	# 		<br/><h3>You can close this window</h3>"""
	# 	self.failure_html = """
	# 		<h1>ERROR: %s</h1><br/><h3>You can close this window</h3>%s"""
	@cherrypy.expose
	def gps(self):
		cl = cherrypy.request.headers['Content-Length']
		rawbody = cherrypy.request.body.read(int(cl))
		print rawbody
		print type(rawbody)
		body = json.loads(rawbody)
		for i in range(len(body)):
			latitude = float(body[i]['latitude'])
			longitude = float(body[i]['longitude'])
			timestamp = body[i]['timestamp']
			db.insert_gps_data(cherrypy.session['user_id'], latitude, longitude, timestamp)
		return rawbody

	@cherrypy.expose
	def login(self, code=None, error=None):
		#some_string = ''.join(random.sample(string.hexdigits, int(length)))
		#cherrypy.session['token'] = some_string
		error = None
		print code
		if code:
			self.oauth.fetch_access_token(code, self.redirect_uri)
		# Use a thread to shutdown cherrypy so we can return HTML first
		return 'hi'

	def _fmt_failure(self, message):
		tb = traceback.format_tb(sys.exc_info()[2])
		tb_html = '<pre>%s</pre>' % ('\n'.join(tb)) if tb else ''
		return self.failure_html % (message, tb_html)

#	def login(self):
#		raise cherrypy.HTTPRedirect('')

if __name__ == '__main__':
	conf = {
		'/': {
			'tools.sessions.on': True,
			'tools.sessions.storage_class': cherrypy.lib.sessions.FileSession,
			'tools.sessions.storage_path': "/sessions"
		}
	}
	cherrypy.config.update({'server.socket_host':'127.0.0.1',
		'server.socket_port':8080,
		})
	cherrypy.quickstart(fitbit(), '/', conf)
