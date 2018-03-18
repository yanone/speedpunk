import unicodedata

def codepages():


	from os import walk
	import os, traceback
	from ynlib.files import ReadFromFile


	ignore = [127, 65535, 63648]

	_codepages = {}

	f = []
	for (dirpath, dirnames, filenames) in walk('/Users/yanone/Schriften/Font Produktion/FontLab/Codepage'):
		
		for filename in filenames:
			try:
				codepage = ReadFromFile(os.path.join(dirpath, filename))

				for line in codepage.split('\n'):
					if 'FONTLAB CODEPAGE' in line:
						codepageName = line.split('; ')[1].strip()
						_codepages[codepageName] = []

					value = None

					if '\t' in line and line.split('\t')[1].startswith('0x'):
						value = int(line.split('\t')[1][2:], 16)

					elif '  ' in line and line.split('  ')[1].startswith('0x'):
						value = int(line.split('  ')[1][2:], 16)

					elif ' ' in line and line.split(' ')[1].startswith('0x'):
						value = int(line.split(' ')[1][2:], 16)

					if value and value >= 32 and not value in ignore and unicodedata.category(unichr(value)) != 'Cc':
						_codepages[codepageName].append(value)

			except:
				pass



	return _codepages
