def GetHTTP(url, timeout = 5):
	u"""GET HTTP responses from the net. Returns False if attempt failed."""

	import urllib2
	try:
		request = urllib2.urlopen(url, timeout = timeout)
		if request.getcode() == 200:
			return request.read()
		else:
			return False
	except:
		return False

def PostHTTP(url, values):
	u"""POST HTTP responses from the net. Values are dictionary {argument: value}"""

	import urllib
	import urllib2

	data = urllib.urlencode(values)
	req = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	return response.read()


def WhatsMyIP():
	u"""Pull your network's public IP address from the net, using whatsmyip.net"""

	import re
	whatsmyiphtml = GetHTTP("http://whatsmyip.net/")
	if whatsmyiphtml:
		m = re.search("""Your <acronym title="Internet Protocol">IP</acronym> Address is: <span>(.+?)</span>""", whatsmyiphtml)
		return m.group(1)
	else:
		return False
