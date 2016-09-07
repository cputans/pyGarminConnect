#!/usr/bin/python

import requests
import re
 
class GarminConnect:
	username = None
	password = None
	session = None

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.loginURL = 'https://sso.garmin.com/sso/login'
		self.searchURL = 'https://connect.garmin.com/proxy/activity-search-service-1.0/json/activities'

	def _login(self):
		if self.session is None:
			self.session = requests.Session()

		ticket = None
		lt = None

		''' Get lt value - this seems to default to 'e1s1' but just to be on the safe side '''
		resp = self.session.get(self.loginURL, 
			allow_redirects=False, 
			params={'service':'https://connect.garmin.com/post-auth/login', 'clientId':'GarminConnect', 'consumeServiceTicket':'false'})

		ltMatch = re.compile('flowExecutionKey: \[([^\]]*)\]').search(resp.text)
		if ltMatch: 
			lt = ltMatch.group(1)
		else:
			raise Exception('Can not acquire lt value')

		''' Get ticket value '''
		resp = self.session.post(self.loginURL, 
			params={'service':'https://connect.garmin.com/post-auth/login', 'clientId':'GarminConnect', 'consumeServiceTicket':'false'}, 
			data={'username':self.username, 'password':self.password, '_eventId':'submit', 'embed':'true', 'lt':lt, 'displayNameRequired':'false'})

		ticketMatch = re.compile("ticket=([^']*)").search(resp.text)
		if ticketMatch:
			ticket = ticketMatch.group(1)
		else:
			raise Exception('Can not acquire ticket value')

		''' Authenticate with ticket'''
		resp = self.session.get(self.loginURL,
			params={'ticket':ticket})

		if resp.status_code == 200:
			''' Make an additional request to the main endpoint emulate a browser connection '''
			self.session.get('https://connect.garmin.com')

			return True
		else:
			raise Exception('Unable to authenticate: %s' % resp.text)


	def getActivities(self, start=0, count=10):
		''' Verify successful auth '''
		if self._login():
			resp = self.session.get(self.searchURL,
				params={'start': start, 'limit':count})

			print resp.json()

		else:
			raise Exception('Unable to authenticate')
