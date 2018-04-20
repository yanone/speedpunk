# encoding: utf-8

##########################################################################################
#
#	SpeedPunk 1.1
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

import objc, webbrowser
from GlyphsApp import *
from GlyphsApp.plugins import *
from AppKit import NSGraphicsContext, NSUserDefaultsController

import speedpunk.speedpunklib

# import cProfile, pstats
# def gprofile(self, layer, command):
	
# 	filename = 'profile_stats.stats'
# 	#profile.run(command, filename)
# 	cProfile.runctx(command, globals(), locals(), filename)

# 	# Read all 5 stats files into a single object
# 	stats = pstats.Stats(filename)
# 	# Clean up filenames for the report
# 	stats.strip_dirs()
# 	# Sort the statistics by the cumulative time spent in the function
# 	stats.sort_stats('cumulative')
# 	stats.print_stats()

class GlyphsAppSpeedPunkReporter(ReporterPlugin):
	
	settingsView = objc.IBOutlet()
	gainSlider = objc.IBOutlet()
	
	def settings(self):

		self.keyboardShortcut = 'x'

		curveGain = speedpunk.speedpunklib.curveGain
		Glyphs.registerDefault('de_yanone_speedPunk_curveGain', speedpunk.speedpunklib.Interpolate(curveGain[0], curveGain[1], .2))
		Glyphs.registerDefault('de_yanone_speedPunk_fader', 1.0)
		
		self.loadNib('settingsView', __file__)
		self.menuName = 'Speed Punk'
		self.speedpunklib = speedpunk.speedpunklib.SpeedPunkLib()
		self.speedpunklib.tool = self
		self.generalContextMenus = [{'name': 'Speed Punk', 'view': self.settingsView}]
		self.gainSlider.setMinValue_(speedpunk.speedpunklib.curveGain[0])
		self.gainSlider.setMaxValue_(speedpunk.speedpunklib.curveGain[1])
		
		self.histWidth = 200
		self.histHeight = 20
		
		default = NSUserDefaultsController.sharedUserDefaultsController()
		default.addObserver_forKeyPath_options_context_(self, 'values.de_yanone_speedPunk_illustrationPositionIndex', 0, None)
		default.addObserver_forKeyPath_options_context_(self, 'values.de_yanone_speedPunk_curveGain', 0, None)
		default.addObserver_forKeyPath_options_context_(self, 'values.de_yanone_speedPunk_useFader', 0, None)
		default.addObserver_forKeyPath_options_context_(self, 'values.de_yanone_speedPunk_fader', 0, None)
	
	def observeValueForKeyPath_ofObject_change_context_(self, keypath, observed, changed, context):
		self.speedpunklib.loadPreferences()
		Glyphs.redraw()
	
	def background(self, layer):
		self.speedpunklib.UpdateGlyph(layer)

	def drawForegroundWithOptions_(self, options):
		if self.speedpunklib.getPreference('useFader'):
			visibleRect = self.controller.viewPort
			histOriginX = NSMinX(visibleRect) + 10
			histOriginY = NSMaxY(visibleRect) - 10 - self.histHeight
			NSGraphicsContext.currentContext().saveGraphicsState()
			clippingPath = NSBezierPath.bezierPathWithRoundedRect_cornerRadius_(NSRect((histOriginX, histOriginY), (self.histWidth, self.histHeight)), 5)
			clippingPath.addClip()
			self.speedpunklib.drawGradient(histOriginX, histOriginY, self.histWidth, self.histHeight)
			self.speedpunklib.drawHistogram(histOriginX, histOriginY, self.histWidth, self.histHeight)
			NSGraphicsContext.currentContext().restoreGraphicsState()
	
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

	@objc.IBAction
	def visitWebsite_(self, sender):
		webbrowser.open_new_tab('https://yanone.de')

	@objc.IBAction
	def visitTwitter_(self, sender):
		webbrowser.open_new_tab('https://twitter.com/yanone')
