def AutoLinkString(string):
	u"""\
	Autlink text with <a> tags to various destinations, such as:
	- Twitter @names and #hashtags
	- Web links (starting with http)
	"""
	import re

	# http
	string = re.sub("((http://|https://|www\.)([a-zA-Z0-9._\/-?=&]+))", "<a target=\"_blank\" href=\"\\1\">\\1</a>", string)
	# Twitter @
	string = re.sub("@([a-zA-Z0-9_]+)", "@<a target=\"_blank\" href=\"http://twitter.com/\\1\">\\1</a>", string)
	# Twitter #
	string = re.sub("#([a-zA-Z0-9._\-]+)", "#<a target=\"_blank\" href=\"http://twitter.com/#search?q=%23\\1\">\\1</a>", string)
	return string

def NaturalWeedkayTimeAndDate(timestamp):
	u"""\
	Return date and time as:
	Wednesday, October 20th, 2010 at 14:12
	"""
	import time

	ordinals = {
	1: 'st',
	2: 'nd',
	3: 'rd',
	21: 'st',
	22: 'nd',
	23: 'rd',
	31: 'st',
	}

	# day without leading zero
	day = time.strftime("%d", time.localtime(timestamp))
	if day.startswith("0"):
		day = day[-1]

	# right ordinal for day
	ordinal = 'th'
	if int(day) in ordinals:
		ordinal = ordinals[int(day)]
	
	return time.strftime("%A, %B " + day + ordinal + ", %Y at %H:%M", time.localtime(timestamp))

def NaturalRelativeWeedkayTimeAndDate(timestamp):
	u"""\
	Return date and time relative to current moment as:
	- x seconds ago
	- x minutes ago
	- x hours ago
	- Wednesday, October 20th, 2010 at 14:12
	"""
	import time
	
	now = time.time()
	timepassed = now - timestamp
	
	if timepassed < 60: # less than 1 minute
		seconds = int(timepassed)
		if seconds == 1:
			return "1 second ago"
		else:
			return "%s seconds ago" % (seconds)
	elif 60 < timepassed < (60 * 60): # 22 minutes ago
		minutes = int(timepassed // 60)
		if minutes == 1:
			return "1 minute ago"
		else:
			return "%s minutes ago" % (minutes)
	elif (60 * 60) < timepassed < (60 * 60 * 24 * 1): # 22 hours ago
		hours = int(timepassed // (60 * 60))
		if hours == 1:
			return "1 hour ago"
		else:
			return "%s hours ago" % (hours)
			
	else:
		return NaturalWeedkayTimeAndDate(timestamp)


def NaturalAmountOfTime(seconds):
	u"""\
	Return years, months, days, hours, minutes and seconds of certain amount of seconds.
	over 2 months
	over 1 day
	over 3 hours
	"""


	second = 1
	minute = 60 * second
	hour = 60 * minute
	day = 24 * hour
	month = 30 * day
	year = 12 * month
	
	if seconds > year:
		years = seconds // year
		if years > 1:
			return "over %s years" % (years)
		else:
			return "over %s year" % (years)
	elif seconds > month:
		months = seconds // month
		if months > 1:
			return "over %s months" % (months)
		else:
			return "over %s month" % (months)
	elif seconds > day:
		days = seconds // day
		if days > 1:
			return "over %s days" % (days)
		else:
			return "over %s day" % (days)
	elif seconds > hour:
		hours = seconds // hour
		if hours > 1:
			return "over %s hours" % (hours)
		else:
			return "over %s hour" % (hours)
	elif seconds > minute:
		minutes = seconds // minute
		if minutes > 1:
			return "over %s minutes" % (minutes)
		else:
			return "over %s minute" % (minutes)
	else:
		if seconds > 1:
			return "%s seconds" % (seconds)
		else:
			return "%s second" % (seconds)


def Garbage(length, uppercase = True, lowercase = True, numbers = True, punctuation = False):
	u"""\
	Return string containing garbage.
	"""
	
	import random
	
	uppercaseparts = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
	lowercaseparts = 'abcdefghijklmnopqrstuvwxyz'
	numberparts = '0123456789'
	punctuationparts = '.-_'
	
	pool = ''
	if uppercase:
		pool += uppercaseparts
	if lowercase:
		pool += lowercaseparts
	if numbers:
		pool += numberparts
	if punctuation:
		pool += punctuationparts
	
	if not pool:
		pool = lowercaseparts
	
	garbage = ''
	
	while len(garbage) < length:
		garbage += random.choice(pool)
	
	return garbage
		
