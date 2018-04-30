def ReadFromFile(path):
	u"""\
	Return content of file
	"""
	import os
	if os.path.exists(path):
		f = open(path, 'r')
		text = f.read()
		f.close()
		return text

def WriteToFile(path, string):
	u"""\
	Write content to file
	"""
	f = open(path, 'w')
	f.write(string)
	f.close()
	return True
