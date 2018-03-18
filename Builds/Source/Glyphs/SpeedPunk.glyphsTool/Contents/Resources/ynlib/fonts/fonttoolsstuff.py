# -*- coding: utf-8 -*-

import fontTools.ttLib
import os, copy
from ynlib.system import Execute


class Glyph(object):
	def __init__(self, parent, name, _unicode = None):
		self.parent = parent
		self.name = name
		self.unicode = _unicode

		# To be set later
		self._bounds = None
		self.width = self.parent.TTFont.getGlyphSet()[self.name].width

	
	def __repr__(self):
		return "<ftGlyph '%s' %s>" % (self.name, self.unicode)

	def bounds(self):
		if not self._bounds:
			from fontTools.pens.boundsPen import BoundsPen, ControlBoundsPen
			pen = BoundsPen(self.parent.TTFont.getGlyphSet())
			self.parent.TTFont.getGlyphSet()[self.name].draw(pen)
			self._bounds = pen.bounds
		return self._bounds

class Font(object):
	def __init__(self, path, recalcTimestamp = True):
		self.path = path
		self.TTFont = fontTools.ttLib.TTFont(self.path, recalcTimestamp = recalcTimestamp)

		self._glyphNames = []
		self._unicodes = []
		self._glyphClasses = []

		self._glyphs = {}
		for table in self.TTFont["cmap"].tables:
			for cmapEntry in table.cmap.items():
				self._addGlyph(cmapEntry[1], cmapEntry[0])

		self.postScriptName = str(self.TTFont['name'].getName(6, 1, 0, 0))

	def version(self):
		return str(self.TTFont['name'].getName(6, 1, 0, 0)).split(';')[0]

	def __repr__(self):
		return "<ftFont '%s'>" % (os.path.basename(self.path))

	def _addGlyph(self, name, _unicode):
		if not name in self._glyphNames:
			self._glyphs[name] = Glyph(self, name, _unicode)
#			self._glyphNames.append(name)

	def tableChecksums(self):
		import md5
		checksums = {}
		for key in self.TTFont.keys():
			try:
				checksums[key] = md5.new(self.TTFont.getTableData(key)).hexdigest()
			except:
				checksums[key] = 'n/a'
		return checksums

	def glyphs(self):
		# Return all glyphs as list
		return [self._glyphs[x] for x in self._glyphs.keys()]

	def glyphNames(self):
		return self.TTFont.getGlyphNames()

	def glyph(self, key):
		# Return single glyph
		if self._glyphs.has_key(key):
			return self._glyphs[key]
		# by Unicode
		else:
			for glyph in self.glyphs():
				if key == glyph.unicode:
					return glyph

	def unicodes(self):
		if not self._unicodes:
			for g in self.glyphs():
				if g.unicode:
					self._unicodes.append(g.unicode)
		return self._unicodes

	def features(self):
		_features = []
		for i, lookup in enumerate(self.TTFont['GSUB'].table.LookupList.Lookup):
			for featureRecord in self.TTFont['GSUB'].table.FeatureList.FeatureRecord:
				if not featureRecord.FeatureTag in _features and i in featureRecord.Feature.LookupListIndex:
					_features.append(featureRecord.FeatureTag)
					break
		for i, lookup in enumerate(self.TTFont['GPOS'].table.LookupList.Lookup):
			for featureRecord in self.TTFont['GPOS'].table.FeatureList.FeatureRecord:
				if not featureRecord.FeatureTag in _features and i in featureRecord.Feature.LookupListIndex:
					_features.append(featureRecord.FeatureTag)
					break
		return _features

	def lookupsPerFeature(self, featureName):
		_lookups = []
		for l, lookup in enumerate(self.TTFont['GSUB'].table.LookupList.Lookup):
			for featureRecord in self.TTFont['GSUB'].table.FeatureList.FeatureRecord:
				if l in featureRecord.Feature.LookupListIndex and featureRecord.FeatureTag == featureName:
					for i in range(lookup.SubTableCount):
						_lookups.append([featureRecord, lookup.SubTable[i]])
		for l, lookup in enumerate(self.TTFont['GPOS'].table.LookupList.Lookup):
			for featureRecord in self.TTFont['GPOS'].table.FeatureList.FeatureRecord:
				if l in featureRecord.Feature.LookupListIndex and featureRecord.FeatureTag == featureName:
					for i in range(lookup.SubTableCount):
						_lookups.append([featureRecord, lookup.SubTable[i]])
		return _lookups

	def stylisticSetName(self, feature):
		for r in self.TTFont['GSUB'].table.FeatureList.FeatureRecord:
			if r.FeatureTag == feature:
				if hasattr(r.Feature.FeatureParams, 'UINameID'):
					return str(self.TTFont['name'].getName(r.Feature.FeatureParams.UINameID, 1, 0, 0))


	def defaultNumerals(self):
		n = ['.osf', '.tosf', '.lf', '.tf']
		for g in self.TTFont.getGlyphNames():
			if '.osf' in g and '.osf' in n:
				n.remove('.osf')
			if '.tosf' in g and '.tosf' in n:
				n.remove('.tosf')
			if '.lf' in g and '.lf' in n:
				n.remove('.lf')
			if '.tf' in g and '.tf' in n:
				n.remove('.tf')
		return n[0].replace('.', '')

	def numerals(self):
		has = []
		num = ['.osf', '.tosf', '.lf', '.tf']
		for g in self.TTFont.getGlyphNames():
			for n in num:
				if n in g and not n in has:
					has.append(n)
		return [x.replace('.', '') for x in has]

	def glyphClasses(self):
		if not self._glyphClasses:
			for g in self.TTFont.getGlyphNames():


				parts = g.split('.')
				for part in parts[1:]:
					if not part in self._glyphClasses:
						self._glyphClasses.append(part)
		return self._glyphClasses

	def bounds(self):
		return self.boundsWithGlyphs(self.glyphs())

	def boundsByUnicodes(self, unicodes):
		_glyphs = []
		for glyph in self.glyphs():
			if glyph.unicode in unicodes:
				_glyphs.append(glyph)
		return self.boundsWithGlyphs(_glyphs)

	def boundsWithGlyphs(self, glyphs):
		left = None
		bottom = None
		right = None
		top = None

		for glyph in glyphs:
			bounds = glyph.bounds()
			if bounds:
				if not left:
					left = bounds[0]
				else:
					left = min(left, bounds[0])
				if not bottom:
					bottom = bounds[1]
				else:
					bottom = min(bottom, bounds[1])
				if not right:
					right = bounds[2]
				else:
					right = max(right, bounds[2])
				if not top:
					top = bounds[3]
				else:
					top = max(top, bounds[3])

		return left, bottom, right, top

	def UIReady(self, top, bottom, feature):

		# Step 1: Find oversize glyphs
		oversize = []
		for glyph in self.glyphs():
			bounds = glyph.bounds()
			if bounds != None:
				if bounds[1] < bottom or bounds[3] > top:
					oversize.append(glyph)


		# Step 2: Check for duplicates of oversize glyphs
		duplicates = []
		for glyph in oversize:
			if self.glyph(glyph.name + '.' + feature):
				glyph = self.glyph(glyph.name + '.' + feature)

				bounds = glyph.bounds()
				if bounds != None:
					if bounds[1] >= bottom and bounds[3] <= top:
						duplicates.append(glyph)
			
		ready = len(oversize) == len(duplicates)
		if not ready:
			print set(oversize) - set(duplicates)
		return ready


	def scripts(self):
		_scripts = []
		for scriptRecord in self.TTFont['GSUB'].table.ScriptList.ScriptRecord:
			_scripts.append(scriptRecord.ScriptTag)
		return _scripts

	def languages(self):
		_languages = []
		for scriptRecord in self.TTFont['GSUB'].table.ScriptList.ScriptRecord:
			for langSys in scriptRecord.Script.LangSysRecord:
				lang = langSys.LangSysTag.strip()
				if not lang in _languages:
					_languages.append(lang)

		return _languages

	def lookupsPerFeatureScriptAndLanguage(self, featureName, scriptName = None, languageName = None):
		_features = []
		for scriptRecord in self.TTFont['GSUB'].table.ScriptList.ScriptRecord:
#			print vars(scriptRecord.Script)
			
			_features.extend(scriptRecord.Script.DefaultLangSys.FeatureIndex)

			if scriptName:

				for languageSystem in scriptRecord.Script.LangSysRecord:
					if scriptRecord.ScriptTag == scriptName:
						if languageSystem.LangSysTag.strip() == languageName:
							_features.extend(languageSystem.LangSys.FeatureIndex)
#			else:
				#	print languageSystem

#		print _features

		_subTables = []
		for i in _features:
			if self.TTFont['GSUB'].table.FeatureList.FeatureRecord[i].FeatureTag == featureName:
				featureTag = self.TTFont['GSUB'].table.FeatureList.FeatureRecord[i]
				for lookupIndex in featureTag.Feature.LookupListIndex:
					lookup = self.TTFont['GSUB'].table.LookupList.Lookup[lookupIndex]
					return lookup.SubTable

		return []

	def featureComparisonString(self, featureName):
#		string = ''
#		print featureName
#		for x in self.lookupsPerFeatureScriptAndLanguage(featureName):
#			print str(vars(x))
		return ''.join([str(vars(x)) for x in self.lookupsPerFeatureScriptAndLanguage(featureName)])

	def shrink(self, freezeFeatures = [], removeFeatures = [], glyphs = [], replaceNames = '', suffix = ''):

			# Freeze features
			from pyftfeatfreeze.pyftfeatfreeze import RemapByOTL
			class FreezeOptions(object):
				pass
			options = FreezeOptions()
			options.inpath = ''
			options.outpath = ''
			options.features = ','.join(freezeFeatures) # comma-separated list of OpenType feature tags, e.g. 'smcp,c2sc,onum'
			options.script = 'latn' # OpenType script tag, e.g. 'cyrl' (default: '%(default)s')
			options.lang = None # OpenType language tag, e.g. 'SRB ' (optional)
			options.zapnames = False # zap glyphnames from the font ('post' table version 3, .ttf only)
			options.rename = True if suffix else False # add a suffix to the font menu names (by default, the suffix will be constructed from the OpenType feature tags)
			options.usesuffix = suffix # use a custom suffix when -S is provided
			options.replacenames = replaceNames # search for strings in the font naming tables and replace them, format is 'search1/replace1,search2/replace2,...'
			options.info = True # update font version string
			options.report = False # report languages, scripts and features in font
			options.names = False # output names of remapped glyphs during processing
			options.verbose = True
			remapByOTL = RemapByOTL(options)
			remapByOTL.ttx = self.TTFont
			remapByOTL.remapByOTL()
			remapByOTL.renameFont()

			# Subset
			from fontTools.subset import Subsetter, Options
#			features = list(set(self.features()) - (set(freezeFeatures) & set(removeFeatures)))
			features = list(set(self.features()) - set(removeFeatures))
#			print 'target features', features
			options = Options(layout_features = features, name_IDs = '*', glyph_names = True, name_legacy = True, name_languages = '*')
			subsetter = Subsetter(options = options)

			# populate with unicodes
			unicodes = []
			for t in self.TTFont['cmap'].tables:
				if t.isUnicode():
					unicodes.extend(t.cmap.keys())
			subsetter.populate(unicodes = unicodes)
			subsetter.subset(self.TTFont)


if __name__ == "__main__":
	import io
	original = '/Users/yanone/Schriften/NonameSans-Regular.otf'
	new = '/Users/yanone/Schriften/NonameSans-Regular-Shrunk.otf'
	newIO = io.BytesIO()
	font = Font(original)

	# Office font
	font.shrink(freezeFeatures = ['tnum', 'lnum', 'zero'], removeFeatures = ['aalt', 'onum', 'pnum', 'smcp', 'c2sc'], suffix = 'Office')

	font.TTFont.save(newIO)

	f = open(new, 'wb')
	f.write(newIO.getvalue())
	f.close()

	print round(os.path.getsize(new) / float(os.path.getsize(original)) * 100), '%'
	font = Font(original)
	newFont = Font(new)
	# for key in font.TTFont.keys():
	# 	try:
	# 		print key, len(font.TTFont.getTableData(key)), len(newFont.TTFont.getTableData(key))
	# 	except:
	# 		pass
	# # print font.TTFont.keys()
	# # print newFont.TTFont.keys()
	# print 'Missing features:', list(set(font.features()) - set(newFont.features()))
	# # print 'Missing glyphs:', list(set(font.glyphNames()) - set(newFont.glyphNames()))
