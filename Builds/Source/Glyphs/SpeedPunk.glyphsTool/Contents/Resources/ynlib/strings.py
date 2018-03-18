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
		return smartString(str(s), encoding, errors, from_encoding)
	elif hasattr(s, '__unicode__'):
		return smartString(unicode(s), encoding, errors, from_encoding)
	else:
		return smartString(str(s), encoding, errors, from_encoding)


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

	string = re.sub(r"\b(http://|https://|www\.)(.+)?", repl, string)
#	string = re.sub(r"\b(http://|https://|www\.)([a-zA-Z0-9-\.\/]+)?", repl, string)

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

def NaturalWeekdayDate(timestamp, locale = 'en'):
	u"""\
	Return date and time as:
	Wednesday, October 20th
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
		return time.strftime("%A, %B " + day + ordinal + " %Y", time.localtime(timestamp))
	elif locale == 'de':
		s = ''
		s += unicode(datelocale[locale][time.strftime("%a", time.localtime(timestamp))]) 
		s += u", "
		s += unicode(day)
		s += u". "
		s += unicode(datelocale[locale][time.strftime("%b", time.localtime(timestamp))])
#		s += unicode(time.strftime(u" %Y um %H:%M Uhr", time.localtime(timestamp)))
		
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
	elif (60 * 60 * 24 * 1) < timepassed < (60 * 60 * 24 * 7):
		days = int(timepassed // (60 * 60 * 24))
		if days == 1:
			answer['en'] = "yesterday"
			answer['de'] = "gestern"
		elif days == 2:
			answer['en'] = "2 days ago"
			answer['de'] = "vorgestern"
		else:
			answer['en'] = "%s days ago" % (days)
			answer['de'] = "vor %s Tagen" % (days)

	# Week
	elif (60 * 60 * 24 * 7 * 1) < timepassed < (60 * 60 * 24 * 7 * 4):
		weeks = int(timepassed // (60 * 60 * 24 * 7 * 1))
		if weeks == 1:
			answer['en'] = "last week"
			answer['de'] = "letzte Woche"
		elif weeks == 2:
			answer['en'] = "2 weeks ago"
			answer['de'] = "vorletzte Woche"
		else:
			answer['en'] = "%s weeks ago" % (weeks)
			answer['de'] = "vor %s Wochen" % (weeks)

	# Month
	elif (60 * 60 * 24 * 30) < timepassed < (60 * 60 * 24 * 365):
		months = int(timepassed // (60 * 60 * 24 * 30))
		if months == 1:
			answer['en'] = "last month"
			answer['de'] = "letzten Monat"
		elif months == 2:
			answer['en'] = "2 months ago"
			answer['de'] = "vorletzten Monat"
		else:
			answer['en'] = "%s months ago" % (months)
			answer['de'] = "vor %s Monaten" % (months)

	# Month
	elif (60 * 60 * 24 * 365) < timepassed:
		years = int(timepassed // (60 * 60 * 24 * 365))
		if years == 1:
			answer['en'] = "1 year ago"
			answer['de'] = "vor 1 Jahr"
		else:
			answer['en'] = "%s years ago" % (years)
			answer['de'] = "vor %s Jahren" % (years)

	if answer.has_key(locale):
		return answer[locale]
	else:
		return NaturalWeekdayTimeAndDate(timestamp, locale)



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
		


def formatPrice(price = 0, currencySymbol = None, numberSeparator = '.', locale = 'en', thousandSeparator = True, decimals = 2):
	



	if price != None:
		if locale == 'de':
			numberSeparator = ','
		else:
			numberSeparator = '.'

		if thousandSeparator:
			thousandSeparator = [',', '.']
			thousandSeparator.remove(numberSeparator)
			thousandSeparator = thousandSeparator[0]
		else:
			thousandSeparator = ''
	
		price *= 10 ** decimals
		price = round(price)
		price /= float(10 ** decimals)

		string = str(float(price))
	
		# negative
		negative = ''
		if string.startswith('-'):
			negative = '-'
			string = string[1:]

		# Fill with zeros
		parts = string.split('.')
		parts[1] = parts[1].ljust(decimals, '0')

	
		part0 = []
		for i in range(1, len(parts[0])+1, 3):
			part0.append(parts[0][max(len(parts[0]) - i - 2, 0) : len(parts[0]) - i + 1])
		part0.reverse()
	
		string = negative + thousandSeparator.join(part0) + numberSeparator + parts[1][:decimals]
		string = string.replace('-', '–&#x2060;')
	
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

def MixedCase(string):
	u"""\
	Generate Mixed Case String
	"""

	parts = string.split(' ')
	newParts = []
	for i in range(len(parts)):
		parts[i] = parts[i][0:1].upper() + parts[i][1:].lower()
	return ' '.join(parts)

def HoursMinutesSeconds(seconds):

	string = ''

	hours = seconds // 3600
	if hours:
		string += '%sh ' % (int(hours))
	seconds -= hours * 3600

	minutes = seconds // 60
	if minutes:
		string += "%s' " % (int(minutes))
	seconds -= minutes * 60

	string += '%s"' % (int(seconds))

	return string

def CleanFloat(number, locale = 'en'):
	u"""\
	Return number without decimal points if .0, otherwise with .x)
	"""
	try:
		if number % 1 == 0:
			return str(int(number))
		else:
			return str(float(number))
	except:
		pass


# https://www.khtt.net/en/page/1821/the-big-kashida-secret

def kashidas(string, length):

	if length > len(string):

		finalAndIsolatedOnly = [u'ء', u'ا', u'إ', u'ٳ', u'د', u'ذ', u'ڈ', u'ڌ', u'ڍ', u'ډ', u'ڊ', u'ڋ', u'ڎ', u'ڏ', u'ڐ', u'ۮ', u'ݙ', u'ݚ', u'ر', u'ز', u'ڑ', u'ڒ', u'ړ', u'ڔ', u'ڕ', u'ږ', u'ڗ', u'ژ', u'ڙ', u'ۯ', u'ݛ', u'ݫ', u'ݬ', u'ﻻ', u'ﻹ', u'و', u'ۄ', u'ۊ', u'ۏ', u'ؤ', u'ۅ', u'ۆ', u'ۇ', u'ۈ', u'ۉ', u'ۋ', u'ٷ']


		add = u'ـ' * (length - len(string))

		# 1. after a kashida that is manually placed in the text by the user,
		if u'ـ' in string:
			pos = string.find(u'ـ')
			# print '#1'
			return string[:pos] + add + string[pos:]

		# 2. after a Seen or Sad (initial and medial form),
		letters = [u'س', u'ص', u'ښ', u'ڛ', u'ش', u'ۺ', u'ڜ', u'ﺺ', u'ڝ', u'ڞ', u'ض', u'ݜ', u'ݭ']
		for i, letter in enumerate(reversed(string)):
			pos = len(string) - i - 1
			if letter in letters:
				# print '#2', string[pos], string[pos+1]
				return string[:pos+1] + add + string[pos+1:]

		# 3. before the final form of Taa Marbutah, Haa, Dal,
		letters = [u'ه', u'ۀ', u'ة', u'ە', u'د', u'ذ', u'ڈ', u'ڌ', u'ڍ', u'ډ', u'ڊ', u'ڋ', u'ڎ', u'ڏ', u'ڐ', u'ۮ', u'ݙ', u'ݚ']
		for i, letter in enumerate(reversed(string)):
			pos = len(string) - i - 1
			if letter in letters:
				if not string[pos-1] in finalAndIsolatedOnly:
					# print '#3', string[pos-1], string[pos]
					return string[:pos] + add + string[pos:]

		# 4. before the final form of Alef, Tah, Lam, Kaf and Gaf,
		letters = [u'ا', u'إ', u'ٳ', u'ب', u'پ', u'ٻ', u'ڀ', u'ت', u'ٽ', u'ث', u'ٹ', u'ٺ', u'ٿ', u'ݐ', u'ݑ', u'ݒ', u'ݓ', u'ݔ', u'ݕ', u'ݖ', u'ك', u'گ', u'ڰ', u'ڴ', u'ڬ', u'ڮ', u'ڲ', u'ڭ', u'ڱ', u'ڳ', u'ل', u'ڸ', u'ݪ']
		for i, letter in enumerate(reversed(string)):
			pos = len(string) - i - 1
			if letter in letters:
				if not string[pos-1] in finalAndIsolatedOnly and string[pos] in finalAndIsolatedOnly:
					# print '#4', string[pos-1], string[pos]
					return string[:pos] + add + string[pos:]

		# 5. before the preceding medial Baa of Ra, Ya and Alef Maqsurah,
		preceding = [u'ٮ', u'ب', u'پ', u'ٻ', u'ڀ', u'ت', u'ٽ', u'ث', u'ٹ', u'ٺ', u'ٿ', u'ݐ', u'ݑ', u'ݒ', u'ݓ', u'ݔ', u'ݕ', u'ݖ', u'ن', u'ں', u'ڻ', u'ڽ', u'ى', u'ي', u'ئ', u'ی', u'ې', u'ۑ', u'ٸ']
		succeeding = [u'ر', u'ز', u'ڑ', u'ڒ', u'ړ', u'ڔ', u'ڕ', u'ږ', u'ڗ', u'ژ', u'ڙ', u'ۯ', u'ݛ', u'ݫ', u'ݬ', u'ى', u'ي', u'ئ', u'ی', u'ې', u'ۑ', u'ٸ']
		for i, letter in enumerate(reversed(string)):
			pos = len(string) - i - 1
			if letter in succeeding:
				if string[pos-1] in preceding and string[pos] in succeeding:
					# print '#5', string[pos-1], string[pos]
					return string[:pos] + add + string[pos:]

		# 6. before the final form of Waw, Ain, Qaf and Fa,
		letters = [u'ع', u'ڠ', u'غ', u'ف', u'ڤ', u'ڡ', u'ڢ', u'ڣ', u'ڥ', u'ڦ', u'ٯ', u'ق', u'ڧ', u'ڨ', u'و', u'ۄ', u'ۊ', u'ۏ', u'ؤ', u'ۅ', u'ۆ', u'ۇ', u'ۈ', u'ۉ', u'ۋ', u'ٷ', u'ݝ', u'ݞ', u'ݟ', u'ݠ', u'ݡ']
		for i, letter in enumerate(reversed(string)):
			pos = len(string) - i - 1

			# letter is at the end of word
			if not string[pos-1] in finalAndIsolatedOnly and i == 0 and letter in letters:
				# print '#6 letter is at the end of word', string[pos-1], string[pos]
				return string[:pos] + add + string[pos:]

			# letter is in middle of word, but final form
			if not string[pos-1] in finalAndIsolatedOnly and string[pos] in letters and string[pos] in finalAndIsolatedOnly:
				# print '#6 final form of letter', string[pos-1], string[pos]
				return string[:pos] + add + string[pos:]

		# 7. before the final form of other characters that can be connected.
		for i, letter in enumerate(reversed(string)):
			pos = len(string) - i - 1
			print pos, string[pos-1], string[pos]

			if not string[pos-1] in finalAndIsolatedOnly:
				# print '#7', string[pos-1], string[pos]
				return string[:pos] + add + string[pos:]

		return string
	else:
		return string


def kashidaSentence(string, length):

	if length > len(string):

		individualLength = int(length / float(len(string.split(' '))))

		sentence = []
		for word in string.split(' '):
			sentence.append(kashidas(word, individualLength))
		return u' '.join(sentence)

	else:
		return string

