# encoding: utf-8
from __future__ import division, print_function, unicode_literals

##########################################################################################
#
#	Speed Punk 1.20
#	Visualisation tool of outline curvature for font editors.
#	
#	Commercial license. Not to be given to other people.
#	
#	Copyright 2012 by Yanone.
#	Web: http://yanone.de
#	Twitter: @yanone
#	Email: post@yanone.de
#
##########################################################################################

import math, time, traceback

from AppKit import NSUserDefaults, NSImage, NSColor, NSBezierPath, NSPoint, NSGradient, NSMakeRect



##########################################################################################
##########################################################################################


def ListPairs(list, num_pairs):
	"""
	Return 'num_pairs' amount of elements of list stacked together as lists.
	Example:
	list = ['a', 'b', 'c', 'd', 'e']
	for one, two, three in ListPairs(list, 3):
		print(one, two, three)
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

def InterpolateHexColorList(colors, p):
	"""
	Interpolate between list of hex RRGGBB values at float position p (0-1)
	Returns float list (R, G, B)
	"""

	# Safety first
	if p < 0: p = 0
	if p > 1: p = 1
	
	if p == 0:
		return colors[0]
	elif p == 1:
		return colors[-1]
	else:
		for i in range(len(colors)):
			
			before = (float(i) / (len(colors) - 1))
			after = (float(i + 1) / (len(colors) - 1))
			
			if  before < p < after:
				v = (p - before) / (after - before)
				
#				print("interpolate between", before, after, p, v)

				R = Interpolate(colors[i][0], colors[i + 1][0], v)
				G = Interpolate(colors[i][1], colors[i + 1][1], v)
				B = Interpolate(colors[i][2], colors[i + 1][2], v)
				return (R, G, B)
			elif p == before:
				return colors[i]
			elif p == after:
				return colors[i + 1]

def Interpolate(a, b, p, limit = False):
	"""
	Interpolate between values a and b at float position p (0-1)
	Limit: No extrapolation
	"""
	i = a + (b - a) * p
	if limit and i < a:
		return a
	elif limit and i > b:
		return b
	else:
		return i

def Execute(command):
	"""
	Execute system command, return output.
	"""

	import sys, os, platform

	if sys.version.startswith("2.3") or platform.system() == "Windows":

		p = os.popen(command, "r")
		response = p.read()
		p.close()
		return response


	else:

		import subprocess

		process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, close_fds=True)
		os.waitpid(process.pid, 0)
		response = process.stdout.read().strip()
		process.stdout.close()
		return response

def Stamina():
	"""
	Calculate system power as integer using by mulitplying number of active CPUs with clock speed.
	"""
	return int(Execute('sysctl hw.activecpu').split(' ')[-1]) * int(Execute('sysctl hw.cpufrequency').split(' ')[-1])

def Environment():
	"""
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


def solveCubicBezier(p1, p2, p3, p4):
	"""
	Solve cubic Bezier equation and 1st and 2nd derivative.
	"""
	a = NSPoint()
	a.x = -p1.x + 3.0 * p2.x - 3.0 * p3.x + p4.x
	a.y = -p1.y + 3.0 * p2.y - 3.0 * p3.y + p4.y
	b = NSPoint()
	b.x = 3.0 * p1.x - 6.0 * p2.x + 3.0 * p3.x
	b.y = 3.0 * p1.y - 6.0 * p2.y + 3.0 * p3.y
	c = NSPoint()
	c.x = -3.0 * p1.x + 3.0 * p2.x
	c.y = -3.0 * p1.y + 3.0 * p2.y
	d = p1
	return a, b, c, d

def solveCubicBezierCurvature(a, b, c, d, t):
	"""
	Calc curvature using cubic Bezier equation and 1st and 2nd derivative.
	Returns position of on-curve point p1234, and vector of 1st and 2nd derivative.
	"""
	r = NSPoint()
	t3 = t**3
	t2 = t**2
	r.x = a.x*t3 + b.x*t2 + c.x*t + d.x
	r.y = a.y*t3 + b.y*t2 + c.y*t + d.y
	
	r1 = NSPoint()
	r1.x = 3*a.x*t2 + 2*b.x*t + c.x
	r1.y = 3*a.y*t2 + 2*b.y*t + c.y
	
	r2 = NSPoint()
	r2.x = 6*a.x*t + 2*b.x
	r2.y = 6*a.y*t + 2*b.y
	
	return (r, r1, r2, (r1.x * r2.y - r1.y * r2.x) / (r1.x**2 + r1.y**2)**1.5)


##########################################################################################
##########################################################################################


environment = Environment()
colors = {
	'cubic': ('8b939c', 'f29400', 'e3004f'),
	'quadratic': ('8b939c', 'f29400', '006f9b')
	}

colors = {
	'cubic': (
		(int("8b", 16) / 255.0, int("93", 16) / 255.0, int("9c", 16) / 255.0),
		(int("f2", 16) / 255.0, int("94", 16) / 255.0, int("00", 16) / 255.0),
		(int("e3", 16) / 255.0, int("00", 16) / 255.0, int("4f", 16) / 255.0)
	),
	'quadratic': (
		(int("8b", 16) / 255.0, int("93", 16) / 255.0, int("9c", 16) / 255.0),
		(int("f2", 16) / 255.0, int("94", 16) / 255.0, int("00", 16) / 255.0),
		(int("00", 16) / 255.0, int("6f", 16) / 255.0, int("9b", 16) / 255.0)
	)
}

c = colors['cubic']
cs = (NSColor.colorWithCalibratedRed_green_blue_alpha_(c[0][0], c[0][1], c[0][2], 0.7), NSColor.colorWithCalibratedRed_green_blue_alpha_(c[1][0], c[1][1], c[1][2], 0.7), NSColor.colorWithCalibratedRed_green_blue_alpha_(c[2][0], c[2][1], c[2][2], 0.7))
cubicGradient = NSGradient.alloc().initWithColors_(cs)

c = colors['quadratic']
cs = (NSColor.colorWithCalibratedRed_green_blue_alpha_(c[0][0], c[0][1], c[0][2], 0.7), NSColor.colorWithCalibratedRed_green_blue_alpha_(c[1][0], c[1][1], c[1][2], 0.7), NSColor.colorWithCalibratedRed_green_blue_alpha_(c[2][0], c[2][1], c[2][2], 0.7))
quadraticGradient = NSGradient.alloc().initWithColors_(cs)

gradients = {
	'cubic': cubicGradient,
	'quadratic' : quadraticGradient
}

curveGain = (.1, 3)
drawfactor = .01

outsideOfGlyph = 0 # index of selected radio button
outsideOfCurve = 1

try:
	TOTALSEGMENTS = min(int(Stamina() * .00000008), 1000)
except:
	TOTALSEGMENTS = 400
MINSEGMENTS = 5
VERSION = '1.2'

if environment == 'RoboFont':
	from lib.tools.bezierTools import curveConverter

elif environment == 'GlyphsApp':
	import GlyphsApp
	from GlyphsApp import Glyphs, Message, CURVE




class SpeedPunkLib(object):
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
		self.preferenceKeys = ('illustrationPositionIndex', 'curveGain', 'useFader', 'fader')
		self.unitsperem = 1000
		self.curves = 'cubic'
		
		self.loadPreferences()

		# Preferences
		justInstalled = False
		if not self.getPreference('illustrationPositionIndex'):
			self.setPreference('illustrationPositionIndex', 1)
			justInstalled = True
		if not self.getPreference('curveGain'):
			self.setPreference('curveGain', Interpolate(curveGain[0], curveGain[1], .2))
			justInstalled = True
		self.setPreference('fader', 1.0)
		self.setPreference('useFader', False)
		self.savePreferences()
		'''
		# UI
		
		self.prefwindow = SpeedPunkPrefWindow(self)
		self.drawGradientImage()
		'''

		## Welcome
		if justInstalled and environment == 'GlyphsApp':
			Message(
			message = Glyphs.localize({
				'en': 'Thank you for choosing Speed Punk. You’ll find me in the View menu under ‘Show Speed Punk’ or with the keyboard shortcut Cmd+Shift+X. The plug-in settings have moved into the context menu (right click).\n\nEnjoy and make sure to follow @yanone on Twitter.',
				'de': 'Danke zur Wahl von Speed Punk. Du findest mich im Ansicht-Menü unter ‘Speed Punk anzeigen’ oder mit dem Tastenkürzel Cmd+Shift+X. Die Plug-in-Einstellungen sind ins Kontextmenü (Rechtsklick) gewandert.\n\nViel Spaß und wir sehen uns bei @yanone auf Twitter.',
				'fr': 'Merci d’avoir choisi Speed Punk. Retrouvez-le dans le menu Affichage sous ‘Afficher Speed Punk’ ou avec le raccourci Cmd+Shift+X. Les préférences se trouvent dans le menu contextuel (clic-droit).\n\nProfitez-en et suivez-moi sur Twitter: @yanone.',
				'es': '¡Gracias por instalar Speed Punk! Lo encontrarás en el menú «Vista > Mostrar Speed Punk» o con el atajo de teclado Cmd+Shift+X. Botón derecho para ver las preferencias. ¡Disfrútalo! Puedes seguirme en Twitter: @yanone.',
				'pt': 'Obrigado por instalar o Speed Punk! Você o encontrará no menu «Visualizar > Exibir Speed Punk» ou com o atalho de teclado Cmd+Shift+X. Clique com o botão direito do mouse para ver as preferências. Aproveite! Você pode me seguir no Twitter: @yanone.',
				# 'jp': 'Thank you for choosing Speed Punk. You’ll find me in the View menu under ‘Show Speed Punk’ or with the keyboard shortcut Cmd+Shift+X. The plug-in settings have moved into the context menu (right click).\n\nEnjoy and make sure to follow @yanone on Twitter.',
				'ko': '“Speed Punk”를 사용해주셔서 감사합니다. 상단메뉴의 ’보기 > Speed Punk 보기’ 클릭 또는 단축키 Cmd + Shift + X로 실행할 수 있습니다. 플러그인 설정은 마우스 오른쪽 > 컨텍스트 메뉴에 있습니다.\n\n트위터에서 @yanone 를 팔로우 해주시기 바랍니다.',
			}),
			title = Glyphs.localize({
				'en': 'Welcome to Speed Punk %s' % VERSION,
				'de': 'Willkommen zu Speed Punk %s' % VERSION,
				'fr': 'Bienvenu·e·s chez Speed Punk %s' % VERSION,
				'es': 'Bienvenido a Speed Punk %s' % VERSION,
				'pt': 'Bem-vindo ao Speed Punk %s' % VERSION,
				# 'jp': 'Welcome to Speed Punk %s' % VERSION,
				'ko': '“Speed Punk %s”를 사용해주셔서 감사합니다.' % VERSION,
			}),
			)
			
		return

	def getPreference(self, key):
		if key in self.preferences:
			return self.preferences[key]
		
	def setPreference(self, key, value):
		self.preferences[key] = value

	def loadPreferences(self):
		for key in self.preferenceKeys:
			value = NSUserDefaults.standardUserDefaults().objectForKey_("de.yanone.speedPunk.%s" % (key))
			self.preferences[key] = value
			setattr(self, key, value)
		
	def savePreferences(self):
		for key in self.preferenceKeys:
			if key in self.preferences:
				NSUserDefaults.standardUserDefaults().setObject_forKey_(self.preferences[key], "de.yanone.speedPunk.%s" % (key))
	
	def Open(self):
		self.prefwindow.w.show()
		self.RefreshView()
	
	def Close(self):
		self.tool.Close()
		self.prefwindow.w.hide()

	def RefreshView(self):
		if environment == 'GlyphsApp':
			GlyphsApp.Glyphs.redraw()
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
				idx = 0
				for n in p.nodes:
					if n.type == CURVE:
						p1 = p.nodes[idx - 3].position
						p2 = p.nodes[idx - 2].position
						p3 = p.nodes[idx - 1].position
						p4 = n.position
						newSegmentPositions.append((p1, p2, p3, p4))
					idx += 1
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
		
	def calcNumberofcurvesegments(self, g):
		numberofcurvesegments = 0
		if environment == 'GlyphsApp':
			for p in g.paths:
				for n in p.nodes:
					if n.type == CURVE:
						numberofcurvesegments += 1
		elif environment == 'RoboFont':
			for c in g:
				for s in c:
					if 'curve' in s.type:
						numberofcurvesegments += 1
		return numberofcurvesegments

	def UpdateGlyph(self, g, glyphstring = None):

		# Units per em
		if environment == 'GlyphsApp':
			self.unitsperem = g.parent.parent.upm
		elif environment == 'RoboFont':
			self.unitsperem = g.getParent().info.unitsPerEm

		# Compare string to see if glyph changed
		if (glyphstring and glyphstring != self.glyphstring) or not glyphstring:
			if glyphstring:
				self.glyphstring = glyphstring

			# Number of curve segments, quick gathering
			self.numberofcurvesegments = self.calcNumberofcurvesegments(g)
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

		if self.useFader:
			self.buildHistogram(self.tool.histWidth)
			#self.drawHistogramImage()

		for segment in self.curvesegments:
			segment.DrawSegment()
		
		# Reset
		self.glyphchanged = False

	def iterateSegments(self):
		for segment in self.curvesegments:
			segment.DrawSegment()
		
	def drawGradientImage(self):
		
		width = int(self.prefwindow.w.gradientImage.getNSImageView().frame().size[0])
		height = int(self.prefwindow.w.gradientImage.getNSImageView().frame().size[1])
		image = NSImage.alloc().initWithSize_((width, height))
		image.lockFocus()
		
		self.drawGradient(0, 0, width, height)
		
		image.unlockFocus()
		self.prefwindow.w.gradientImage.setImage(imageObject=image)
		
	def drawGradient(self, originX, originY, width, height):
		gradient = gradients[self.curves]
		gradient.drawInRect_angle_(NSMakeRect(originX, originY, width, height), 0)

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

	def drawHistogramImage(self):
		width = int(self.tool.histWidth)
		height = int(self.tool.histHeight)
		
		image = NSImage.alloc().initWithSize_((width, height))
		image.lockFocus()
		image.setBackgroundColor_(NSColor.clearColor())
		self.drawHistogram(0, 0, width, height)
		image.unlockFocus()
		self.prefwindow.w.histogramImage.setImage(imageObject=image)
	
	def drawHistogram(self, originX, originY, width, height):
		NSColor.colorWithWhite_alpha_(0, .5).set()
		path = NSBezierPath.bezierPath()
		path.moveToPoint_((originX, originY - 2))
		prevY = 0
		for x in range(width):
			if x in self.histogram:
				y = (self.histogram[x] / float(self.maxhistogram)) * height
				path.lineToPoint_((x + .5 + originX, y + originY))
			else:
				path.lineToPoint_((x + .5 + originX, originY - 2))
		path.lineToPoint_((originX + width, originY - 2))
		path.closePath()
		path.fill()

class Curvature:
	def __init__(self, segment, set1, set2):
		self.segment = segment
		self.set1 = set1
		self.set2 = set2
		self.curveGain = None
		self.illustrationPosition = None
		self.fader = None
		self.useFader = None
		
	def DrawCurvature(self):
		
		# Color
		self._DrawCurvatureColor()
		self._DrawCurvatureIllustration()
		return self._DrawCurvaturePaths()
	
	def _DrawCurvatureColor(self):
		prefFader = self.segment.speedpunklib.fader
		prefUseFader = self.segment.speedpunklib.useFader
		if self.segment.speedpunklib.glyphchanged or self.fader != prefFader or self.useFader != prefUseFader:
			#print("__color")
			self.fader = prefFader
			self.useFader = prefUseFader
			
			# Color
			p = (self.Value() - self.segment.speedpunklib.vmin) / (self.segment.speedpunklib.vmax - self.segment.speedpunklib.vmin)
			R, G, B = InterpolateHexColorList(colors[self.segment.speedpunklib.curves], p)


			# Fader
			faderMin = .2
			faderMax = .7
			if prefUseFader:
				# Alpha
				fader = prefFader
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

	def _DrawCurvatureIllustration(self):
		# Recalc illustration
		prefIllustrationPositionIndex = int(self.segment.speedpunklib.illustrationPositionIndex)
		prefCurveGain = self.segment.speedpunklib.curveGain
		
		if self.segment.speedpunklib.glyphchanged or self.curveGain != prefCurveGain or self.illustrationPosition != prefIllustrationPositionIndex:
			#print("__illustration")
			self.curveGain = prefCurveGain
			self.illustrationPosition = prefIllustrationPositionIndex
			
			k1 = self.set1[3] * drawfactor * self.curveGain * self.segment.speedpunklib.unitsperem**2
			k2 = self.set2[3] * drawfactor * self.curveGain * self.segment.speedpunklib.unitsperem**2

			if self.illustrationPosition == outsideOfGlyph:
				k1 = abs(k1)
				k2 = abs(k2)
			
				# TrueType
				if self.segment.speedpunklib.curves == 'quadratic':
					k1 *= -1
					k2 *= -1

			# Define points
			S10 = self.set1[0]
			S11 = self.set1[1]
			S20 = self.set2[0]
			S21 = self.set2[1]
			self.oncurve1 = S10
			self.oncurve2 = S20
			S21abs = math.sqrt(S21.x**2 + S21.y**2)
			S11abs = math.sqrt(S11.x**2 + S11.y**2)
			self.outerspace2 = (S20.x + (S21.y / S21abs * k2), S20.y - (S21.x / S21abs * k2))
			self.outerspace1 = (S10.x + (S11.y / S11abs * k1), S10.y - (S11.x / S11abs * k1))
		
			self.path = NSBezierPath.bezierPath()
			# OnCurve
			self.path.moveToPoint_(self.oncurve1)
			self.path.lineToPoint_(self.oncurve2)
			# Outer points
			self.path.lineToPoint_(self.outerspace2)
			self.path.lineToPoint_(self.outerspace1)
			self.path.closePath()
	
	def _DrawCurvaturePaths(self):
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
		steps = int(max(TOTALSEGMENTS / self.speedpunklib.numberofcurvesegments, MINSEGMENTS - 1))
		
		self.curvatureSets = []
		
		sets = []
		a, b, c, d = solveCubicBezier(p1, p2, p3, p4)
		for i in range(steps + 1):
			t = i / float(steps)
			#r, r1, r2 = solveCubicBezier(p1, p2, p3, p4, t)
			try:
				result = solveCubicBezierCurvature(a, b, c, d, t)
				sets.append(result)
			except:
				pass
		for set1, set2 in ListPairs(sets, 2):
			self.curvatureSets.append(Curvature(self, set1, set2))
			
	
	def DrawSegment(self):
		drawcount = 0
		for set in self.curvatureSets:
			drawcount += set.DrawCurvature()
		return drawcount

	def Values(self):
		values = []
		for set in self.curvatureSets:
			values.append(set.Value())
		return values
