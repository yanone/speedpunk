import plistlib, os

class Preferences(object):
	def __init__(self, appKey = None, path = None):
		self.appKey = appKey
		self.preferences = {}

		# plist
		if path:
			self.plistfile = path
		else:
			self.plistfile = os.path.join(os.path.expanduser("~/Library/Preferences/"), self.appKey + '.plist')
		
		self.loadPreferences()
		
		self.modified = False
		
	def get(self, key):
		if self.preferences.has_key(key):
			return self.preferences[key]
		
	def put(self, key, value):
		if value != self.get(key):
			self.modified = True

		self.preferences[key] = value

		if self.modified == True:
			self.savePreferences()

	def max(self, key, value):
		
		if value > self.get(key):
			self.put(key, value)

	def min(self, key, value):
		if value < self.get(key):
			self.put(key, value)
	
	def delete(self, key):
		if self.preferences.has_key(key):
			self.preferences.pop(key)
		self.savePreferences()

	def loadPreferences(self):
		if os.path.exists(self.plistfile):
			self.preferences = plistlib.readPlist(self.plistfile)
		
	def savePreferences(self):
		plistlib.writePlist(self.preferences, self.plistfile)
