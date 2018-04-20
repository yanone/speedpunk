import fontTools.ttLib


class Glyph(object):
	def __init__(self, parent, name, _unicode = None):
		self.parent = parent
		self.name = name
		self.unicode = _unicode
	
	def __repr__(self):
		return "<Glyph '%s' %s>" % (self.name, self.unicode)

class Font(object):
	def __init__(self, fontfilepath):
		self.fontfilepath = fontfilepath
		self.TTFont = fontTools.ttLib.TTFont(self.fontfilepath)

		self.glyphNames = []

		self.glyphs = []
		for table in self.TTFont["cmap"].tables:
			for cmapEntry in table.cmap.items():
				self._addGlyph(cmapEntry[1], cmapEntry[0])

	def _addGlyph(self, name, _unicode):
		if not name in self.glyphNames:
			self.glyphs.append(Glyph(self, name, _unicode))
			self.glyphNames.append(name)

	def unicodes(self):
		_unicodes = []
		for g in self.glyphs:
			if g.unicode:
				_unicodes.append(g.unicode)
		return _unicodes

