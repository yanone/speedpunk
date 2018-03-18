# -*- coding: utf-8 -*-

import calendar, time

weekend = ['Sat', 'Sun']
locale = 'de'

datelocale = {
	'de': {
		'Jan': u'Januar',
		'Feb': u'Februar',
		'Mar': u'März',
		'Apr': u'April',
		'May': u'Mai',
		'Jun': u'Juni',
		'Jul': u'Juli',
		'Aug': u'August',
		'Sep': u'September',
		'Oct': u'Oktober',
		'Nov': u'November',
		'Dec': u'Dezember',

		'Mon': u'Montag',
		'Tue': u'Dienstag',
		'Wed': u'Mittwoch',
		'Thu': u'Donnerstag',
		'Fri': u'Freitag',
		'Sat': u'Samstag',
		'Sun': u'Sonntag',

		'Karfreitag': 'Karfreitag',
		'Ostermontag': 'Ostermontag',
		'Himmelfahrt': 'Himmelfahrt',
		'Pfingstmontag': 'Pfingstmontag',
		'Neujahr': 'Neujahr',
		},

	'en': {
		'Jan': 'January',
		'Feb': 'February',
		'Mar': 'March',
		'Apr': 'April',
		'May': 'May',
		'Jun': 'June',
		'Jul': 'July',
		'Aug': 'August',
		'Sep': 'September',
		'Oct': 'October',
		'Nov': 'November',
		'Dec': 'December',

		'Mon': 'Monday',
		'Tue': 'Tuesday',
		'Wed': 'Wednesday',
		'Thu': 'Thursday',
		'Fri': 'Friday',
		'Sat': 'Saturday',
		'Sun': 'Sunday',

		'Karfreitag': 'Karfreitag',
		'Ostermontag': 'Ostermontag',
		'Himmelfahrt': 'Himmelfahrt',
		'Pfingstmontag': 'Pfingstmontag',
		},

	'nl': {
		'Jan': 'Januari',
		'Feb': 'Februari',
		'Mar': 'Maart',
		'Apr': 'April',
		'May': 'Mei',
		'Jun': 'Juni',
		'Jul': 'Juli',
		'Aug': 'Augustus',
		'Sep': 'September',
		'Oct': 'October',
		'Nov': 'November',
		'Dec': 'December',

		'Mon': 'Maandag',
		'Tue': 'Dinsdag',
		'Wed': 'Woensdag',
		'Thu': 'Donderdag',
		'Fri': 'Vrijdag',
		'Sat': 'Zaterdag',
		'Sun': 'Zondag',

		'Karfreitag': 'Karfreitag',
		'Ostermontag': 'Ostermontag',
		'Himmelfahrt': 'Himmelfahrt',
		'Pfingstmontag': 'Pfingstmontag',
		},
}
specialdays = {
#	'17 Mar 2011': 'Presentation #2',
	}


class Year:
	def __init__(self, year, locale = locale, recurse = True):
		self.year = year
		self.locale = locale
		self.recurse = recurse
		
		self.easter = Easter(self.year)
		self.holidays = {
		# Fest
			Day(self.year, 1, 1, withholidays = False): 'Neujahr',
			Day(self.year, 5, 1, withholidays = False): 'Maifeiertag',
			Day(self.year, 10, 3, withholidays = False): 'Tag der Deutschen Einheit',
			Day(self.year, 12, 25, withholidays = False): '1. und 2. Weihnachtsfeiertag',
			Day(self.year, 12, 26, withholidays = False): '',

		# Schwimmend
			self.easter - 2: 'Karfreitag',
			self.easter + 1: 'Ostermontag',
			self.easter + 39: 'Christi Himmelfahrt',
			self.easter + 50: 'Pfingstmontag',
		}

		if self.recurse:
			self.months = []
			for i in range(1, 13):
				self.months.append(Month(self.year, i, locale = self.locale, yearobject = self))
		
	def __repr__(self):
	    return "<Year %s>" % (self.year)


class Month:
	def __init__(self, year, month, locale = locale, yearobject = None):
		import calendar
		self.year = year
		self.yearobject = yearobject
		self.month = month
		self.locale = locale

		self.timestamp = time.mktime(time.strptime("01 " + str(self.month).zfill(2) + " " + str(self.year), "%d %m %Y")) + 60*60*12
		self.daysInMonth = calendar.monthrange(self.year, self.month)[1]
		self.name = datelocale[self.locale][time.strftime("%b", time.gmtime(self.timestamp))]
	
		self.days = []
		for i in range(1, self.daysInMonth + 1):
			self.days.append(Day(self.year, self.month , i, locale = self.locale, monthobject = self, yearobject = self.yearobject))

	def __repr__(self):
	    return "<Month %s %s>" % (self.year, self.name)


class Day:
	def __init__(self, year, month, day, locale = locale, monthobject = None, yearobject = None, withholidays = True):
		self.year = year
		if yearobject:
			self.yearobject = yearobject
		else:
			#self.yearobject = Year(self.year, recurse = False)
			self.yearobject = None
		self.month = month
		self.monthobject = monthobject
		self.day = day
		self.locale = locale
		self.withholidays = withholidays
		
		self.timestamp = time.mktime(time.strptime(str(self.day).zfill(2) + " " + str(self.month).zfill(2) + " " + str(self.year), "%d %m %Y")) + 60*60*12

		self.weekday = datelocale[self.locale][time.strftime("%a", time.gmtime(self.timestamp))]
		
		# Weekend
		if time.strftime("%a", time.gmtime(self.timestamp)) in weekend:
			self.weekend = True
		else:
			self.weekend = False
		
		# Today
		if time.strftime("%d %b %Y", time.gmtime(self.timestamp)) == time.strftime("%d %b %Y", time.gmtime(time.time())):
			self.today = True
		else:
			self.today = False

		if withholidays and self.yearobject:
#			if time.strftime("%d %b", time.gmtime(self.timestamp)) in fixedholidays.keys():
#				self.holiday = True
#				self.holidayname = fixedholidays[time.strftime("%d %b", time.gmtime(self.timestamp))]

			if self in self.yearobject.holidays:

				self.holiday = True
				self.holidayname = self.yearobject.holidays[self]
				#self.holidayname = datelocale[self.locale][self.yearobject.holidays[self]]
				#self.holidayname = 'Ostern'

			else:
				self.holiday = False
				self.holidayname = None

			# Special Day
			if time.strftime("%d %b %Y", time.gmtime(self.timestamp)) in specialdays.keys():
				self.specialday = True
				self.specialdayname = specialdays[time.strftime("%d %b %Y", time.gmtime(self.timestamp))]
			else:
				self.specialday = False
				self.specialdayname = None
		


	def __repr__(self):
	    return "<Day %s-%s-%s>" % (self.year, self.month, self.day)
	
	def __add__(self, other):
		if isinstance(other, int):
			newdate = time.localtime(self.timestamp + other*60*60*24)
			return Day(newdate[0], newdate[1], newdate[2], withholidays = self.withholidays)

	def __sub__(self, other):
		if isinstance(other, int):
			newdate = time.localtime(self.timestamp - other*60*60*24)
			return Day(newdate[0], newdate[1], newdate[2], withholidays = self.withholidays)

	def __cmp__(self, other):
		return hash(self) != hash(other)

	def __hash__(self):
		return int(str(self.year)+str(self.month).zfill(2)+str(self.day).zfill(2))


def Easter(year):
	"""Date of Christian Easter"""
	a = year % 19
	b = year // 100
	c = year % 100
	d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
	e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
	f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
	month = f // 31
	day = f % 31 + 1	
	return Day(year, month, day, withholidays = False)
