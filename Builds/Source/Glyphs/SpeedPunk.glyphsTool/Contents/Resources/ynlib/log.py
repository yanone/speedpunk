import syslog

def Log(text, identifier = 'Python'):
	# Define identifier
	syslog.openlog(identifier)
	# Record a message
	syslog.syslog(syslog.LOG_ALERT, text)