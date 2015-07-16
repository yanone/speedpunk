from mojo.events import BaseEventTool, installTool, EditingTool

################################################################################################################
# Speed Punk, v0.1a
# (c) 2011 Yanone
# http://yanone.de
################################################################################################################

##INSERTCODE##

import speedpunk
from speedpunk.speedpunklib import *
reload(speedpunk.speedpunklib)
from AppKit import *
from mojo.extensions import ExtensionBundle
bundle = ExtensionBundle("SpeedPunk")

################################################################################################################

speedpunkib = SpeedPunkLib()

class SpeedPunkTool(EditingTool):
	

	def becomeActive(self):
		
		self.speedpunklib = speedpunkib
		self.speedpunklib.tool = self
		self.speedpunklib.Open()
	
	def drawBackground(self, scale):
		
		if self.getGlyph() != None:
			self.speedpunklib.UpdateGlyph(self.getGlyph())

	def becomeInactive(self):
		self.speedpunklib.Close()
	
	def glyphWindowWillClose(self, a):
		self.speedpunklib.Close()

	def glyphWindowDidOpen(self, a):
		self.speedpunklib.Open()

	def getToolbarTip(self):
		return "Speed Punk"
	
	def getToolbarIcon(self):
		NSImage = bundle.getResourceImage("toolbar", "png")
		print NSImage
		if NSImage:
			return NSImage

installTool(SpeedPunkTool())