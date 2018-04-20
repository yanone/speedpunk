import compositor, time





# store open files
compositorfontfiles = {}
maxcompositorfontfiles = 50

def CompFont(fontfilepath):
	from operator import itemgetter

	global compositorfontfiles

	# Sort
	sortedcompositorfontfiles = sorted(compositorfontfiles.iteritems(), key=itemgetter(1))
	
	if not fontfilepath in compositorfontfiles:
		compositorfontfiles[fontfilepath] = [time.time(), compositor.Font(fontfilepath)]

	# Set new timestamp
	compositorfontfiles[fontfilepath][0] = time.time()

	# Delete oldest objects
	while len(compositorfontfiles) > maxcompositorfontfiles:
#		compositorfontfiles.pop(sortedcompositorfontfiles.pop(0))
#		sortedcompositorfontfiles.pop(0)
		del compositorfontfiles[sortedcompositorfontfiles[0][0]]

	return compositorfontfiles[fontfilepath][1]


def Process(fontfilepath, string, features = None):
	u"""\
	Process a string on a font file using compositor. Returns (glyphsets, glyphrecords).
	"""

	returnlist = []
	
	font = CompFont(fontfilepath)
	
	# Apply features
	if features:
		for feature in features:
			font.setFeatureState(feature, True)

	# Process
	glyphrecords = font.process(string)
	for glyphrecord in glyphrecords:
		returnlist.append((font.glyphSet[glyphrecord.glyphName], glyphrecord))
	
	return returnlist

def BoundingBox(glyphset):
	u"""\
	Calculate Bounding Box with BoundingBoxPen
	"""
	
	from ynlib.pens import BoundingBoxPen
	bboxpen = BoundingBoxPen(glyphset)
	glyphset.draw(bboxpen)
	
	return bboxpen

def TextWidth(fontfilepath, string, features = None):
	u"""\
	Process a string and return complete width.
	"""
	width = 0
	glyphs = Process(fontfilepath, string, features)

	for glyphset, glyphrecord in glyphs:
	    width += glyphset.width
	return width
