# encoding: utf-8
from __future__ import division, print_function, unicode_literals

##########################################################################################
#
#	Speed Punk
#	Visualisation tool of outline curvature for font editors.
#	
#	Distributed under Apache 2.0 license
#
##########################################################################################

import objc, webbrowser
from GlyphsApp import *
from GlyphsApp import NSStr
from GlyphsApp.plugins import *
from Foundation import NSString
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
	
	@objc.python_method
	def settings(self):
		self.keyboardShortcut = 'x'

		curveGain = speedpunk.speedpunklib.curveGain
		self.loadNib('settingsView', __file__)
		self.menuName = 'Speed Punk'
		self.speedpunklib = speedpunk.speedpunklib.SpeedPunkLib()
		self.speedpunklib.tool = self
		self.generalContextMenus = [{'name': 'Speed Punk', 'view': self.settingsView}]
		self.gainSlider.setMinValue_(curveGain[0])
		self.gainSlider.setMaxValue_(curveGain[1])
		
		self.histWidth = 200
		self.histHeight = 20
		
		default = NSUserDefaultsController.sharedUserDefaultsController()
		default.addObserver_forKeyPath_options_context_(self, NSStr('values.de.yanone.speedPunk.illustrationPositionIndex'), 0, None)
		default.addObserver_forKeyPath_options_context_(self, NSStr('values.de.yanone.speedPunk.curveGain'), 0, None)
		default.addObserver_forKeyPath_options_context_(self, NSStr('values.de.yanone.speedPunk.useFader'), 0, None)
		default.addObserver_forKeyPath_options_context_(self, NSStr('values.de.yanone.speedPunk.fader'), 0, None)
	
	@objc.python_method
	def conditionsAreMetForDrawing(self):
			"""
			Don't activate if text or pan (hand) tool are active.
			"""
			currentController = self.controller.view().window().windowController()
			if currentController:
				tool = currentController.toolDrawDelegate()
				textToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolText") )
				handToolIsActive = tool.isKindOfClass_( NSClassFromString("GlyphsToolHand") )
				if not textToolIsActive and not handToolIsActive: 
					return True
			return False
	
	def observeValueForKeyPath_ofObject_change_context_(self, keypath, observed, changed, context):
		self.speedpunklib.loadPreferences()
		Glyphs.redraw()
	
	@objc.python_method
	def background(self, layer):
		if self.conditionsAreMetForDrawing():
			self.speedpunklib.UpdateGlyph(layer)

	def drawForegroundWithOptions_(self, options):
		if self.speedpunklib.useFader:
			visibleRect = self.controller.viewPort
			histOriginX = NSMinX(visibleRect) + 10
			histOriginY = NSMaxY(visibleRect) - 10 - self.histHeight
			NSGraphicsContext.currentContext().saveGraphicsState()
			clippingPath = NSBezierPath.bezierPathWithRoundedRect_cornerRadius_(NSRect((histOriginX, histOriginY), (self.histWidth, self.histHeight)), 5)
			clippingPath.addClip()
			self.speedpunklib.drawGradient(histOriginX, histOriginY, self.histWidth, self.histHeight)
			self.speedpunklib.drawHistogram(histOriginX, histOriginY, self.histWidth, self.histHeight)
			NSGraphicsContext.currentContext().restoreGraphicsState()
	
	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__

	@objc.IBAction
	def visitWebsite_(self, sender):
		webbrowser.open_new_tab('https://github.com/yanone/speedpunk')

	@objc.IBAction
	def visitTwitter_(self, sender):
		webbrowser.open_new_tab('https://twitter.com/yanone')
