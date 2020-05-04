##########################################################################################
#
#	Speed Punk
#	Visualisation tool of outline curvature for font editors.
#	
#	Distributed under Apache 2.0 license
#
##########################################################################################

import time, os, math, sys, plistlib, traceback

import vanilla
from AppKit import NSBezierPath, NSColor, NSBundle, NSUserDefaults, NSImage, NSLog


##########################################################################################


def Environment():
	"""\
	Return the environment, from which this script is being called.
	Currently supported: FontLab, GlyphsApp, NodeBox, Python
	"""

	environment = 'Python'

	try:
		import FL
		environment = 'FontLab'
	except: pass

	try:
		from AppKit import NSBundle
		MainBundle = NSBundle.mainBundle()
		if 'Glyphs' in MainBundle.bundlePath():
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

def Stamina():
	"""\
	Calculate system power as integer using by mulitplying number of active CPUs with clock speed.
	"""
	from ynlib.system import Execute
	return int(Execute('sysctl hw.activecpu').split(' ')[-1]) * int(Execute('sysctl hw.cpufrequency').split(' ')[-1])

def Interpolate(a, b, p):
	"""\
	Interpolate between values a and b at float position p (0-1)
	"""
	return a + (b - a) * p


def InterpolateHexColorList(colors, p):
	"""\
	Interpolate between list of hex RRGGBB values at float position p (0-1)
	Returns float list (R, G, B)
	"""

	#from ynlib.maths import Interpolate

	# Safety first
	if p < 0: p = 0
	if p > 1: p = 1

	if p == 0:
		return (int(colors[0][0:2], 16) / 255.0, int(colors[0][2:4], 16) / 255.0, int(colors[0][4:6], 16) / 255.0)
	elif p == 1:
		return (int(colors[-1][0:2], 16) / 255.0, int(colors[-1][2:4], 16) / 255.0, int(colors[-1][4:6], 16) / 255.0)
	else:
		for i in range(len(colors)):

			before = (float(i) / (len(colors) - 1))
			after = (float(i + 1) / (len(colors) - 1))

			if  before < p < after:
				v = (p - before) / (after - before)

#				print "interpolate between", before, after, p, v

				R = Interpolate(int(colors[i][0:2], 16) / 255.0, int(colors[i + 1][0:2], 16) / 255.0, v)
				G = Interpolate(int(colors[i][2:4], 16) / 255.0, int(colors[i + 1][2:4], 16) / 255.0, v)
				B = Interpolate(int(colors[i][4:6], 16) / 255.0, int(colors[i + 1][4:6], 16) / 255.0, v)
				return (R, G, B)
			elif p == before:
				return (int(colors[i][0:2], 16) / 255.0, int(colors[i][2:4], 16) / 255.0, int(colors[i][4:6], 16) / 255.0)
			elif p == after:
				return (int(colors[i + 1][0:2], 16) / 255.0, int(colors[i + 1][2:4], 16) / 255.0, int(colors[i + 1][4:6], 16) / 255.0)


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(self.x + other.x, self.y + other.y)

	__radd__ = __add__

	def __sub__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(self.x - other.x, self.y - other.y)

	def __rsub__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(other.x - self.x, other.y - self.y)

	def __mul__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(self.x * other.x, self.y * other.y)

	__rmul__ = __mul__

	def __div__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(self.x / other.x, self.y / other.y)

	def __rdiv__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(other.x / self.x, other.y / self.y)

	def __abs__(self):
		return math.sqrt(self.x**2 + self.y**2)


	def __neg__(self):
		return Point(-self.x, -self.y)

#	def __cmp__(self, other):
#		c = hash(other) - hash(self)
#		if not isinstance(c, int):
#			c = int(-1)
#		return c

	def __eq__(self, other):
	    return (self.x, self.y) == (other.x, other.y)

	def __ne__(self, other):
	    return (self.x, self.y) != (other.x, other.y)

	def __hash__(self):
		return hash((self.x, self.y))

	def __repr__(self):
		return '<Point %s %s>' % (self.x, self.y)


def solveCubicBezier(p1, p2, p3, p4, t):
	"""\
	Solve cubic Bezier equation and 1st and 2nd derivative.
	Returns position of on-curve point p1234, and vector of 1st and 2nd derivative.
	"""
	a = -p1 + 3.0 * p2 - 3.0 * p3 + p4
	b = 3.0 * p1 - 6.0 * p2 + 3.0 * p3
	c = -3.0 * p1 + 3.0 * p2
	d = p1

	r = a*t**3 + b*t**2 + c*t + d
	r1 = 3*a*t**2 + 2*b*t + c
	r2 = 6*a*t + 2*b

	return r, r1, r2

def solveCubicBezierCurvature(r, r1, r2):
	"""\
	Calc curvature using cubic Bezier equation and 1st and 2nd derivative.
	"""
	return (r1.x * r2.y - r1.y * r2.x) / (r1.x**2 + r1.y**2)**1.5


def ListPairs(list, num_pairs):
	"""\
	Return 'num_pairs' amount of elements of list stacked together as lists.
	Example:
	list = ['a', 'b', 'c', 'd', 'e']
	for one, two, three in ListPairs(list, 3):
		print one, two, three
	a b c
	b c d
	c d e
	"""
	returnlist = []

	for i in range(len(list) - num_pairs + 1):

		singlereturnlist = []
		for j in range(num_pairs):
			singlereturnlist.append(list[i + j])

		returnlist.extend([singlereturnlist])

	return returnlist



##########################################################################################



environment = Environment()
colors = {
	'cubic': ('8b939c', 'f29400', 'e3004f'),
	'quadratic': ('8b939c', 'f29400', '006f9b')
	}
curveGain = (.1, 3)
drawfactor = .01
try:
	TOTALSEGMENTS = min(int(Stamina() * .00000008), 1000)
except:
	TOTALSEGMENTS = 400
MINSEGMENTS = 5

if sys.version_info.major < 3:
	plist = plistlib.readPlist(os.path.join(os.path.dirname(__file__), '..', '..', 'info.plist'))
else:
	with open(os.path.join(os.path.dirname(__file__), '..', '..', 'info.plist'), 'rb') as pl_file:
		plist = plistlib.load(pl_file)
VERSION = plist['version']

if environment == 'RoboFont':
	from lib.tools.bezierTools import curveConverter

elif environment == 'GlyphsApp':
	MainBundle = NSBundle.mainBundle()
	path = MainBundle.bundlePath()+"/Contents/Scripts"
	if not path in sys.path:
		sys.path.append(path)
	import GlyphsApp



##########################################################################################


class SpeedPunkLib:
	def __init__(self):

		self.tool = None
		self.curvesegments = []
		self.values = []
		self.vmin = None
		self.vmax = None
		self.histogram = {}
		self.glyphchanged = False
		self.numberofcurvesegments = 0
		self.glyphstring = None
		self.preferences = {}
		self.preferenceKeys = ('illustrationPosition', 'curveGain')
		self.unitsperem = 1000
		self.curves = 'cubic'

		self.loadPreferences()

		# Preferences
		if not self.getPreference('illustrationPosition'):
			self.setPreference('illustrationPosition', 'outsideOfGlyph')
		if not self.getPreference('curveGain'):
			self.setPreference('curveGain', Interpolate(curveGain[0], curveGain[1], .2))
		self.setPreference('fader', 1.0)
		self.setPreference('useFader', False)

		# UI
		self.prefwindow = SpeedPunkPrefWindow(self)
		self.drawGradientImage()

	def getPreference(self, key):
		return self.preferences[key]

	def setPreference(self, key, value):
		self.preferences[key] = value

	def loadPreferences(self):
		for key in self.preferenceKeys:
			self.preferences[key] = NSUserDefaults.standardUserDefaults().objectForKey_("de.yanone.speedPunk.%s" % (key))

	def savePreferences(self):
		for key in self.preferenceKeys:
			if key in self.preferences:
				NSUserDefaults.standardUserDefaults().setObject_forKey_(self.preferences[key], "de.yanone.speedPunk.%s" % (key))

	def Open(self):
		self.prefwindow.w.show()
		self.RefreshView()

	def Close(self):
		self.savePreferences()
		self.prefwindow.w.hide()

	def RefreshView(self):
		if environment == 'GlyphsApp':
			if self.tool.editViewController():
				self.tool.editViewController().graphicView().setNeedsDisplay_(True)
#			except: pass
		elif environment == 'RoboFont':
			self.tool.refreshView()

	def gatherSegments(self, g):

		changed = False
		oldSegments = self.curvesegments

		# Compile new curve segments list
		newSegmentPositions = []
		newCurvesType = self.curves

		# Glyphs
		if environment == 'GlyphsApp':
			for p in g.paths:
				for s in p.segments:
					if len(s) == 4:
						pv = s[0].pointValue()
						p1 = Point(pv[0], pv[1])
						pv = s[1].pointValue()
						p2 = Point(pv[0], pv[1])
						pv = s[2].pointValue()
						p3 = Point(pv[0], pv[1])
						pv = s[3].pointValue()
						p4 = Point(pv[0], pv[1])
						newSegmentPositions.append((p1, p2, p3, p4))

		# RoboFont
		elif environment == 'RoboFont':
			for c in g:
				previouspoint = previouspoint = c[-1].points[-1]
				for s in c:
					if s.type == 'curve':
						newCurvesType = 'cubic'
						p1 = Point(previouspoint.x, previouspoint.y)
						p2 = Point(s.points[0].x, s.points[0].y)
						p3 = Point(s.points[1].x, s.points[1].y)
						p4 = Point(s.points[2].x, s.points[2].y)
						newSegmentPositions.append((p1, p2, p3, p4))
					elif s.type == 'qcurve':
						newCurvesType = 'quadratic'
						p1 = Point(previouspoint.x, previouspoint.y)
						p2 = Point(s.points[0].x, s.points[0].y)
						p3 = Point(s.points[1].x, s.points[1].y)
						p4 = Point(s.points[2].x, s.points[2].y)

						(h1x, h1y), (h2x, h2y), (x2, y2) = curveConverter.convertSegment((p1.x, p1.y), ((p2.x, p2.y), (p3.x, p3.y), (p4.x, p4.y)),  "curve")
						p2 = Point(h1x, h1y)
						p3 = Point(h2x, h2y)
						p4 = Point(x2, y2)

						newSegmentPositions.append((p1, p2, p3, p4))

					previouspoint = s.points[-1]

		# Curve type has changed
		if newCurvesType != self.curves:
			self.curves = newCurvesType
			self.drawGradientImage()

		# Compare curvesegments (p1, p2, p3, p4) to list of segments objects.
		if len(newSegmentPositions) != len(oldSegments):
			oldSegments = []
			changed = True
			for curvesegment in newSegmentPositions:
				p1, p2, p3, p4 = curvesegment
				oldSegments.append(Segment(self, p1, p2, p3, p4))

		else:
			# Compare stored segments with new coordinates, recalc if necessary
			for i, curvesegment in enumerate(newSegmentPositions):
				p1, p2, p3, p4 = curvesegment
				if (p1, p2, p3, p4) != (oldSegments[i].p1, oldSegments[i].p2, oldSegments[i].p3, oldSegments[i].p4):
					oldSegments[i] = Segment(self, p1, p2, p3, p4)
					changed = True

		self.curvesegments = oldSegments
		self.glyphchanged = changed

	def UpdateGlyph(self, g, glyphstring = None):

		# Units per em
		if environment == 'GlyphsApp':
			self.unitsperem = g.parent.parent.upm
		elif environment == 'RoboFont':
			self.unitsperem = g.font.info.unitsPerEm

		# Compare string to see if glyph changed
		if (glyphstring and glyphstring != self.glyphstring) or not glyphstring:
			if glyphstring:
				self.glyphstring = glyphstring

			# Number of curve segments, quick gathering
			numberofcurvesegments = 0
			if environment == 'GlyphsApp':
				for p in g.paths:
					for s in p.segments:
						if len(s) == 4:
							numberofcurvesegments += 1
			elif environment == 'RoboFont':
				for c in g:
					for s in c:
						if 'curve' in s.type:
							numberofcurvesegments += 1
			self.numberofcurvesegments = numberofcurvesegments


			# Assign new segments
			self.gatherSegments(g)

			# Things have actually changed
			if self.glyphchanged:
				self.values = []

				for segment in self.curvesegments:
					self.values.extend(segment.Values())

				# Glyph has outlines
				if self.values:
					self.vmin = min(self.values)
					self.vmax = max(self.values)

		# Draw
#		context = NSGraphicsContext.currentContext()
#		context.setCompositingOperation_(12)
#		context.setShouldAntialias_(False)

		if self.getPreference('useFader'):
			self.buildHistogram(self.prefwindow.w.gradientImage.getNSImageView().frame().size[0])
			self.drawHistogram()

		drawcount = 0
		for segment in self.curvesegments:
			drawcount += segment.Draw()

		# Reset
		self.glyphchanged = False

	def drawGradientImage(self):

		width = int(self.prefwindow.w.gradientImage.getNSImageView().frame().size[0])
		height = int(self.prefwindow.w.gradientImage.getNSImageView().frame().size[1])
		image = NSImage.alloc().initWithSize_((width, height))
		image.lockFocus()

		for x in range(width):
			p = x/float(width)
			R, G, B = InterpolateHexColorList(colors[self.curves], p)
			NSColor.colorWithCalibratedRed_green_blue_alpha_(R, G, B, 1.0).set()
			path = NSBezierPath.bezierPath()
			path.moveToPoint_((x, 0))
			path.lineToPoint_((x, height))
			path.stroke()

		image.unlockFocus()
		self.prefwindow.w.gradientImage.setImage(imageObject=image)

	def buildHistogram(self, width):
		self.histogram = {}
		self.maxhistogram = 0
		for v in self.values:
			key = int(Interpolate(1, width, (v - self.vmin) / (self.vmax - self.vmin))) - 1
			if key not in self.histogram:
				self.histogram[key] = 0
			self.histogram[key] += 1
			if self.histogram[key] > self.maxhistogram:
				self.maxhistogram = self.histogram[key]

	def	drawHistogram(self):
		width = int(self.prefwindow.w.histogramImage.getNSImageView().frame().size[0])
		height = int(self.prefwindow.w.histogramImage.getNSImageView().frame().size[1])

		image = NSImage.alloc().initWithSize_((width, height))
		image.lockFocus()
		image.setBackgroundColor_(NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 1, 1, 0))
		NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0, .8).set()

		for x in range(width):
			if x in self.histogram:
				path = NSBezierPath.bezierPath()
				path.moveToPoint_((x + .5, 0))
				y = (self.histogram[x] / float(self.maxhistogram)) * height

				path.lineToPoint_((x + .5, y))
				path.stroke()

		image.unlockFocus()
		self.prefwindow.w.histogramImage.setImage(imageObject=image)


class Curvature:
	def __init__(self, segment, set1, set2):
		self.segment = segment
		self.set1 = set1
		self.set2 = set2
		self.curveGain = None
		self.illustrationPosition = None
		self.fader = None
		self.useFader = None

	def Draw(self):

		# Color
		if self.segment.speedpunklib.glyphchanged or self.fader != self.segment.speedpunklib.getPreference('fader') or self.useFader != self.segment.speedpunklib.getPreference('useFader'):
			self.fader = self.segment.speedpunklib.getPreference('fader')
			self.useFader = self.segment.speedpunklib.getPreference('useFader')

			# Color
			p = (self.Value() - self.segment.speedpunklib.vmin) / (self.segment.speedpunklib.vmax - self.segment.speedpunklib.vmin)
			R, G, B = InterpolateHexColorList(colors[self.segment.speedpunklib.curves], p)


			# Fader
			faderMin = .2
			faderMax = .7
			if self.segment.speedpunklib.getPreference('useFader'):
				# Alpha
				fader = self.segment.speedpunklib.prefwindow.w.faderSlider.get()
				histerese = .2

				if p > fader:
					d = p - fader
					if d > histerese:
						v = 0.0
					else:
						v = 1.0 - d / histerese
				else:
					v = 1.0

				A = Interpolate(faderMin, faderMax, v)
			else:
				A = faderMax


			self.color = NSColor.colorWithCalibratedRed_green_blue_alpha_(R, G, B, A)

		# Recalc illustration
		if self.segment.speedpunklib.glyphchanged or self.curveGain != self.segment.speedpunklib.getPreference('curveGain') or self.illustrationPosition != self.segment.speedpunklib.getPreference('illustrationPosition'):
			self.curveGain = self.segment.speedpunklib.getPreference('curveGain')
			self.illustrationPosition = self.segment.speedpunklib.getPreference('illustrationPosition')

			k1 = self.set1[3] * drawfactor * self.curveGain * self.segment.speedpunklib.unitsperem**2
			k2 = self.set2[3] * drawfactor * self.curveGain * self.segment.speedpunklib.unitsperem**2

			if self.illustrationPosition == 'outsideOfGlyph':
				k1 = abs(k1)
				k2 = abs(k2)

				# TrueType
				if self.segment.speedpunklib.curves == 'quadratic':
					k1 *= -1
					k2 *= -1

			# Define points
			self.oncurve1 = (self.set1[0].x, self.set1[0].y)
			self.oncurve2 = (self.set2[0].x, self.set2[0].y)
			self.outerspace2 = (self.set2[0].x + (self.set2[1].y / abs(self.set2[1]) * k2), self.set2[0].y - (self.set2[1].x / abs(self.set2[1]) * k2))
			self.outerspace1 = (self.set1[0].x + (self.set1[1].y / abs(self.set1[1]) * k1), self.set1[0].y - (self.set1[1].x / abs(self.set1[1]) * k1) )

			self.path = NSBezierPath.bezierPath()
			# OnCurve
			self.path.moveToPoint_(self.oncurve1)
			self.path.lineToPoint_(self.oncurve2)
			# Outer points
			self.path.lineToPoint_(self.outerspace2)
			self.path.lineToPoint_(self.outerspace1)
			self.path.closePath()

		self.color.set()
#		self.path

		self.path.fill()
#		self.path.setLineWidth_(0.2)
#		self.path.stroke()

		return 1

#		else:
#			return 0

	def Value(self):
		return abs(self.set1[3] * drawfactor) + abs(self.set2[3] * drawfactor) / 2.0


class Segment:
	def __init__(self, speedpunklib, p1, p2, p3, p4):

		self.speedpunklib = speedpunklib

		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.p4 = p4

		self.highestvalue = None
		self.lowestvalue = None

		### Calc
		steps = int(round(max(TOTALSEGMENTS / self.speedpunklib.numberofcurvesegments, MINSEGMENTS - 1)))

		self.curvatureSets = []

		sets = []
		for i in range(steps + 1):
			t = i / float(steps)
			r, r1, r2 = solveCubicBezier(p1, p2, p3, p4, t)
			try:
				k = solveCubicBezierCurvature(r, r1, r2)
				sets.append((r, r1, r2, k))
			except:
				pass

		for set1, set2 in ListPairs(sets, 2):
			self.curvatureSets.append(Curvature(self, set1, set2))


	def Draw(self):

		drawcount = 0
		for set in self.curvatureSets:
			drawcount += set.Draw()
		return drawcount

	def Values(self):
		values = []
		for set in self.curvatureSets:
			values.append(set.Value())
		return values



class SpeedPunkPrefWindow(object):

	def __init__(self, parent):
		self.parent = parent
		self.w = vanilla.FloatingWindow((150, 130), "Speed Punk %s" % VERSION,
								closable = False,
								autosaveName = 'de.yanone.speedPunk.%s.prefWindow' % (environment),
								)

		from AppKit import NSHUDWindowMask, NSUtilityWindowMask, NSTitledWindowMask, NSBorderlessWindowMask
		self.w.getNSWindow().setStyleMask_(0 << 1 | 0 << 2 | NSUtilityWindowMask | NSTitledWindowMask | NSBorderlessWindowMask)

		self.w.illustrationPositionRadioGroup = vanilla.RadioGroup((10, 10, -10, 40),
								["Outside of glyph", "Outer side of curve"],
								callback=self.radioGroupCallback,
								sizeStyle = "small")

		self.w.curveGainTextBox = vanilla.TextBox((10, 60, -10, 17), "Gain",
							sizeStyle = "mini")

		self.w.curveGainSlider = vanilla.Slider((10, 70, -10, 25),
							tickMarkCount=5,
							callback=self.curveGainSliderCallback,
							sizeStyle = "small",
							minValue = curveGain[0],
							maxValue = curveGain[1],
							value = self.parent.getPreference('curveGain'))

		if self.parent.getPreference('illustrationPosition') == "outsideOfGlyph": self.w.illustrationPositionRadioGroup.set(0)
		if self.parent.getPreference('illustrationPosition') == "outsideOfCurve": self.w.illustrationPositionRadioGroup.set(1)


		self.w.faderCheckBox = vanilla.CheckBox((10, 100, -10, 17), "Fader",
							sizeStyle = "small",
							callback=self.faderCheckBoxCallback)

		self.w.faderSlider = vanilla.Slider((10, 125, -10, 25),
							sizeStyle = "small",
							minValue = 0,
							maxValue = 1.0,
							value = 1.0,
							callback=self.faderSliderCallback,
							)

		self.w.gradientImage = vanilla.ImageView((10, 150, -10, 15))
		self.w.histogramImage = vanilla.ImageView((10, 150, -10, 15))

	def radioGroupCallback(self, sender):
		illustrationPosition = ("outsideOfGlyph", "outsideOfCurve")
		self.parent.setPreference('illustrationPosition', illustrationPosition[sender.get()])
		self.parent.RefreshView()

	def curveGainSliderCallback(self, sender):
		self.parent.setPreference('curveGain', sender.get())
		self.parent.RefreshView()

	def faderSliderCallback(self, sender):
		self.parent.setPreference('fader', sender.get())
		self.parent.RefreshView()

	def faderCheckBoxCallback(self, sender):
		self.parent.setPreference('useFader', sender.get())
		self.parent.RefreshView()
		if sender.get():
			self.w.faderCheckBox.setPosSize(((10, 105, -10, 17)))
			self.w.resize(150, 175, animate=True)
		else:
			self.w.faderCheckBox.setPosSize(((10, 100, -10, 17)))
			self.w.resize(150, 130, animate=True)

