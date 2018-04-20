# -*- coding: utf-8 -*-


def smartString(s, encoding='utf-8', errors='strict', from_encoding='utf-8'):
	u"""\
	Convert all incoming string to Unicode.
	"""
	import types
	if type(s) in (int, long, float, types.NoneType):
		return str(s)
	elif type(s) is str:
		if encoding != from_encoding:
			return s.decode(from_encoding, errors).encode(encoding, errors)
		else:
			return s
	elif type(s) is unicode:
		return s.encode(encoding, errors)
	elif hasattr(s, '__str__'):
		return self.smartString(str(s), encoding, errors, from_encoding)
	elif hasattr(s, '__unicode__'):
		return self.smartString(unicode(s), encoding, errors, from_encoding)
	else:
		return self.smartString(str(s), encoding, errors, from_encoding)


def feet(height_cms):
	u"""\
	Convert cm to feet and inches.
	"""
	inches = height_cms / 2.54 
	feet = inches / 12 
	remainder_inches = inches % 12 

	return "%d′%d″" % (feet, remainder_inches)


def SimpleTextWrap(text, characters):
	import textwrap
	w = textwrap.TextWrapper()
	w.width = characters
	
	lines = text.split("\n")
	lists = (w.wrap(line) for line in lines)
	body  = "\n".join("\n".join(list) for list in lists)
	return body


def ReadableFileSize(num):
	u"""\
	Makes human readable file size of integer bytes.
	"""
	for x in ['bytes','KB','MB','GB']:
		if num < 1024.0 and num > -1024.0:
			return "%3.1f%s" % (num, x)
		num /= 1024.0
	return "%3.1f%s" % (num, 'TB')


def AutoLinkString(string):
	u"""\
	Autlink text with <a> tags to various destinations, such as:
	- Twitter @names and #hashtags
	- Web links (starting with http)
	"""
	import re

	# email
	string = re.sub("(([a-zA-Z0-9._\-]+)@([a-zA-Z0-9\._-]+))", "<a href=\"mailto:\\1\">\\1</a>", string)

	# http
	def repl(r):
		output = []
		output.append('<a href="')

		http = r.group(1) or 'http://'
		if not http.startswith('http'):
			http  = 'http://' + http

		# remove punctuation at the end
		group2 = r.group(2)
		for s in ['.']:
			group2 = group2.split(s)
			if group2[-1] == '':
				punctuation = s
				group2 = s.join(group2[:-1])
			else:
				punctuation = ''
				group2 = s.join(group2)
			
		
		if '/' in group2:

			domain = group2.split('/')[0]
			path = group2.split('/')[1:]
		
		else:
			domain = group2
			path = ''

		shortDomain = domain.split('.')[-2] + '.' + domain.split('.')[-1]
		URL = http + domain + '/' + '/'.join(path)
		
		output.append(URL)
	
		output.append('">')
		output.append(shortDomain)
		output.append('</a>')
		output.append(punctuation)
	
		return ''.join(output)

	string = re.sub(r"\b(http://|https://|www\.)([a-zA-Z0-9-\.\/]+)?", repl, string)

	return string




ordinals = {
1: 'st',
2: 'nd',
3: 'rd',
21: 'st',
22: 'nd',
23: 'rd',
31: 'st',
}


def FormattedDate(timestamp, locale = 'en'):
	u"""\
	Return date and time as:
	October 20th, 2010
	"""

	import time
	from calendars import datelocale

	# day without leading zero
	day = time.strftime("%d", time.localtime(timestamp))
	if day.startswith("0"):
		day = day[-1]

	# right ordinal for day
	ordinal = 'th'
	if int(day) in ordinals:
		ordinal = ordinals[int(day)]


	if locale == 'en':
		return time.strftime("%B " + day + ordinal + ", %Y", time.localtime(timestamp))
	elif locale == 'de':
		return unicode(day) + u". " + datelocale[locale][time.strftime("%b", time.localtime(timestamp))] + u' ' + time.strftime("%Y", time.localtime(timestamp))


def NaturalWeekdayTimeAndDate(timestamp, locale = 'en'):
	u"""\
	Return date and time as:
	Wednesday, October 20th, 2010 at 14:12
	"""
	import time
	from calendars import datelocale

	# day without leading zero
	day = time.strftime("%d", time.localtime(timestamp))
	if day.startswith("0"):
		day = day[-1]

	# right ordinal for day
	ordinal = 'th'
	if int(day) in ordinals:
		ordinal = ordinals[int(day)]
	
	if locale == 'en':
		return time.strftime("%A, %B " + day + ordinal + ", %Y at %H:%M", time.localtime(timestamp))
	elif locale == 'de':
		s = ''
		s += unicode(datelocale[locale][time.strftime("%a", time.localtime(timestamp))]) 
		s += u", "
		s += unicode(day)
		s += u". "
		s += unicode(datelocale[locale][time.strftime("%b", time.localtime(timestamp))])
		s += unicode(time.strftime(u" %Y um %H:%M Uhr", time.localtime(timestamp)))
		
		return s
#		day + u". " + datelocale[locale][time.strftime("%b", time.localtime(timestamp))] + u" %Y um %H:%M Uhr", time.localtime(timestamp)

def MonthAndYear(timestamp, locale = 'en'):
	u"""\
	Return date:
	May 2012
	"""
	import time
	from calendars import datelocale

	if locale == 'en':
		return time.strftime("%B %Y", time.localtime(timestamp))
	elif locale == 'de':
		return datelocale[locale][time.strftime("%b", time.localtime(timestamp))] + ' ' + time.strftime("%Y", time.localtime(timestamp))

def NaturalRelativeWeekdayTimeAndDate(timestamp, locale = 'en', relativeDays = 14):
	u"""\
	Return date and time relative to current moment as:
	- x seconds ago
	- x minutes ago
	- x hours ago
	- Wednesday, October 20th, 2010 at 14:12
	"""
	import time
	answer = {}
	
	now = time.time()
	timepassed = now - timestamp
	
	if timepassed < 60: # less than 1 minute
		seconds = int(timepassed)
		if seconds == 1:
			answer['en'] = "1 second ago"
			answer['de'] = "vor 1 Sekunde"
		else:
			answer['en'] = "%s seconds ago" % (seconds)
			answer['de'] = "vor %s Sekunden" % (seconds)
	elif 60 < timepassed < (60 * 60): # 22 minutes ago
		minutes = int(timepassed // 60)
		if minutes == 1:
			answer['en'] = "1 minute ago"
			answer['de'] = "vor 1 Minute"
		else:
			answer['en'] = "%s minutes ago" % (minutes)
			answer['de'] = "vor %s Minuten" % (minutes)
	elif (60 * 60) < timepassed < (60 * 60 * 24 * 1): # 22 hours ago
		hours = int(timepassed // (60 * 60))
		if hours == 1:
			answer['en'] = "1 hour ago"
			answer['de'] = "vor 1 Stunde"
		else:
			answer['en'] = "%s hours ago" % (hours)
			answer['de'] = "vor %s Stunden" % (hours)
	elif (60 * 60 * 24 * 1) < timepassed < (60 * 60 * 24 * relativeDays): # 22 hours ago
		days = int(timepassed // (60 * 60 * 24))
		if days == 1:
			answer['en'] = "yesterday"
			answer['de'] = "gestern"
		elif days == 1:
			answer['en'] = "2 days ago"
			answer['de'] = "vorgestern"
		else:
			answer['en'] = "%s days ago" % (days)
			answer['de'] = "vor %s Tagen" % (days)

	if answer.has_key(locale):
		return answer[locale]
	else:
		return NaturalWeedkayTimeAndDate(timestamp, locale)

def NaturalRelativeWeedkayDate(timestamp, locale = 'en', relativeDays = 14):
	u"""\
	Return date and time relative to current moment as:
	- x seconds ago
	- x minutes ago
	- x hours ago
	- Wednesday, October 20th, 2010 at 14:12
	"""
	import time
	answer = {}
	
	now = time.time()
	timepassed = now - timestamp
	
	if timepassed < 60: # less than 1 minute
		seconds = int(timepassed)
		if seconds == 1:
			answer['en'] = "1 second ago"
			answer['de'] = "vor 1 Sekunde"
		else:
			answer['en'] = "%s seconds ago" % (seconds)
			answer['de'] = "vor %s Sekunden" % (seconds)
	elif 60 < timepassed < (60 * 60): # 22 minutes ago
		minutes = int(timepassed // 60)
		if minutes == 1:
			answer['en'] = "1 minute ago"
			answer['de'] = "vor 1 Minute"
		else:
			answer['en'] = "%s minutes ago" % (minutes)
			answer['de'] = "vor %s Minuten" % (minutes)
	elif (60 * 60) < timepassed < (60 * 60 * 24 * 1): # 22 hours ago
		hours = int(timepassed // (60 * 60))
		if hours == 1:
			answer['en'] = "1 hour ago"
			answer['de'] = "vor 1 Stunde"
		else:
			answer['en'] = "%s hours ago" % (hours)
			answer['de'] = "vor %s Stunden" % (hours)
	elif (60 * 60 * 24 * 1) < timepassed < (60 * 60 * 24 * relativeDays): # 22 hours ago
		days = int(timepassed // (60 * 60 * 24))
		if days == 1:
			answer['en'] = "yesterday"
			answer['de'] = "gestern"
		elif days == 1:
			answer['en'] = "2 days ago"
			answer['de'] = "vorgestern"
		else:
			answer['en'] = "%s days ago" % (days)
			answer['de'] = "vor %s Tagen" % (days)

	if answer.has_key(locale):
		return answer[locale]
	else:
		return FormattedDate(timestamp, locale)


def NaturalAmountOfTime(seconds, locale = 'en'):
	u"""\
	Return years, months, days, hours, minutes and seconds of certain amount of seconds.
	over 2 months
	over 1 day
	over 3 hours
	"""

	answer = {}

	second = 1
	minute = 60 * second
	hour = 60 * minute
	day = 24 * hour
	month = 30 * day
	year = 12 * month
	
	if seconds > year:
		years = seconds // year
		if years > 1:
			answer['en'] = "over %s years" % (years)
			answer['de'] = u"über %s Jahre" % (years)
		else:
			answer['en'] = "over 1 year"
			answer['de'] = u"über 1 Jahr"
	elif seconds > month:
		months = seconds // month
		if months > 1:
			answer['en'] = "over %s months" % (months)
			answer['de'] = u"über %s Monate" % (months)
		else:
			answer['en'] = "over 1 month"
			answer['de'] = u"über 1 Monat"
	elif seconds > day:
		days = seconds // day
		if days > 1:
			answer['en'] = "over %s days" % (days)
			answer['de'] = u"über %s Tage" % (days)
		else:
			answer['en'] = "over 1 day"
			answer['de'] = u"über 1 Tag"
	elif seconds > hour:
		hours = seconds // hour
		if hours > 1:
			answer['en'] = "over %s hours" % (hours)
			answer['de'] = u"über %s Stunden" % (hours)
		else:
			answer['en'] = "over 1 hour"
			answer['de'] = u"über 1 Stunde"
	elif seconds > minute:
		minutes = seconds // minute
		if minutes > 1:
			answer['en'] = "over %s minutes" % (minutes)
			answer['de'] = u"über %s Minuten" % (minutes)
		else:
			answer['en'] = "over 1 minute" % (minutes)
			answer['de'] = u"über 1 Minute" % (minutes)
	else:
		if seconds > 1:
			answer['en'] = "%s seconds" % (seconds)
			answer['de'] = "%s Sekunden" % (seconds)
		else:
			answer['en'] = "%s second" % (seconds)
			answer['de'] = "%s Sekunde" % (seconds)

	return answer[locale]

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
		


def formatPrice(price = 0, currencySymbol = None, numberSeparator = '.', locale = 'en'):
	
	if locale == 'de':
		numberSeparator = ','
	else:
		numberSeparator = '.'

	thousandSeparator = [',', '.']
	thousandSeparator.remove(numberSeparator)
	
	price *= 100
	price = round(price)
	price /= 100.0

	string = str(float(price))
	
	# negative
	negative = ''
	if string.startswith('-'):
		negative = '-'
		string = string[1:]

	# Fill with zeros
	parts = string.split('.')
	parts[1] = parts[1].ljust(2, '0')

	
	part0 = []
	for i in range(1, len(parts[0])+1, 3):
		part0.append(parts[0][max(len(parts[0]) - i - 2, 0) : len(parts[0]) - i + 1])
	part0.reverse()
	
	string = negative + thousandSeparator[0].join(part0) + numberSeparator + parts[1][:2]
	string = string.replace('-', '–')
	
	if currencySymbol:
		string += currencySymbol

	return string


def GenitiveS(name, locale = 'en'):
	u"""\
	Apply genitive s rules.
	"""

	if locale == 'de':
		return '’' if name.endswith('s') else 's'
	else:
		return '’' if name.endswith('s') else '’s'
