def CollectFunctions(libraryname, librarypath, code, functioncodedict = {}):
	u"""\
	Collect python functions from external libraries into one single, shippable Python code string.
	'paths' provides a 'libname': 'pathtolib' dictionary,
	'string' is the Python code to be parsed and replaced.
	Returns the new code and a dictionary with the replaced functions.
	"""
	
	import re, os, string
	from ynlib.files import ReadFromFile

	# Match "from library import function"
	m = re.search("(from " + libraryname + "\.(.+?) import (.+?))\n", code)
	i = 0

	while m:	
		i += 1
		
		# RE result processing
		m_wholematch = m.group(1)
		m_libraryname = m.group(2)
		functionstogather = map(string.strip, m.group(3).split(','))

		# Pull Python code from file		
		pythoncodefromfile = ReadFromFile(os.path.join(librarypath, m_libraryname + '.py'))

		# Gather function code one by one
		for function in functionstogather:
			if function not in functioncodedict:
				functioncodedict[function] = GrabFunction(pythoncodefromfile, function)
				
				#Recursion
				functioncodedict[function], newfunctioncodedict = CollectFunctions(libraryname, librarypath, functioncodedict[function], functioncodedict)
				# Add functions back to dict
				for function in newfunctioncodedict:
					if function not in functioncodedict:
						functioncodedict[function] = newfunctioncodedict[function]

		# Replace import statements with comments	
		code = string.replace(code, m_wholematch, '# Function/class grabbed (' + libraryname + '.' + m_libraryname + '): ' + ', '.join(functionstogather))

		# Repeat
		m = re.search("(from " + libraryname + "\.(.+?) import (.+?))\n", code)
		
	# Top level replacement
	if '##INSERTCODE##' in code:
		gatheredfunctioncode = '\n'.join(functioncodedict.values())
		code = string.replace(code, '##INSERTCODE##', gatheredfunctioncode)

	return code, functioncodedict


def GrabFunction(code, function):
	u"""\
	Get and return the code of a function from a string of Python code.
	"""
	
	import re
	m = re.search(r"((def|class) " + function + "(.|\n)*?)(^(def|class) |\Z)", code, re.M)
	if m:	
		return m.group(1)
	

def Environment():
	u"""\
	Return the environment, from which this script is being called.
	Currently supported: FontLab, GlyphsApp, NodeBox, Python
	"""
	
	environment = 'Python'
	
	try:
		import FL
		environment = 'FontLab'
	except: pass

	try:
		import GlyphsApp
		environment = 'GlyphsApp'
	except: pass

	try:
		import mojo
		environment = 'RoboFont'
	except: pass

	try:
		import nodebox
		environment = 'NodeBox'
	except: pass
	
	return environment
