# -*- coding: utf-8 -*-

import time
from strings import *

def convertToEUR(source, amount = 1.0, timestamp = None):
	u"""/
	
	"""
	from web import GetHTTP
	import json


	# Bitcoin
	if source.upper() == 'XBT':
		url = 'https://blockchain.info/tobtc?currency=EUR&value=%s' % amount
		reply = float(GetHTTP(url))
		return True, 1 / reply

	else:

		# STEP 1, confirm currency
		
		url = 'http://www.apilayer.net/api/live?access_key=2c17819a3f130af5f5e867c77a362d27'
		url += '&currencies=%s' % source.upper()
		
		reply = json.loads(GetHTTP(url))
		if reply['success'] == True:

			# historical
			if timestamp != None:
				url = 'http://www.apilayer.net/api/historical?access_key=2c17819a3f130af5f5e867c77a362d27&date=%s-%s-%s' % (time.strftime('%Y', time.gmtime(timestamp)), time.strftime('%m', time.gmtime(timestamp)), time.strftime('%d', time.gmtime(timestamp)))
				url += '&currencies=EUR,%s' % source.upper()


			# live
			else:
				url = 'http://www.apilayer.net/api/live?access_key=2c17819a3f130af5f5e867c77a362d27'
				url += '&currencies=EUR,%s' % source.upper()
				if timestamp:
					url += '&timestamp=%s' % timestamp
		
			reply = json.loads(GetHTTP(url))
		
		
			base = reply['source']
		
			sourceValue = reply['quotes'][base + source.upper()]
			targetValue = reply['quotes'][base + 'EUR']
		
		
			return True, (float(targetValue / sourceValue) * float(amount))
		
		else:
			
			return False, reply['error']['info']
