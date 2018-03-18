def RGlyphFromGlifString(glifString):
	u"""\
	Return RGlyph object directly from .glif file
	"""
	
	from robofab.world import RGlyph
	from robofab.glifLib import readGlyphFromString
	
	glyph = RGlyph()
	readGlyphFromString(glifString, glyph, glyph.getPointPen())
	return glyph


def FakePointStructure(glyph):
	u"""\
	Returns a string representing the outline structure of a glyph, for comparison.
	Not very safe.
	"""

	string = ''
	
	for contour in glyph.contours:
		string += '_'
		
		for segment in contour.segments:
			
			if segment.type == 'line':
				string += 'L'
			if segment.type == 'move':
				string += 'M'
			if segment.type == 'curve':
				string += 'C'
				
	return string
