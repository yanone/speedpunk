##########################################################################################
#
#	SpeedPunk 1.11
#	Visualisation tool of outline curvature for font editors.
#
#	Commercial license. Not to be given to other people.
#
#	Copyright 2012 by Yanone.
#	Web: https://yanone.de
#	Twitter: @yanone
#	Email: post@yanone.de
#
##########################################################################################

from mojo.events import installTool, EditingTool
from deYanoneRoboFontSpeedpunk import speedpunklib
from mojo.extensions import ExtensionBundle
bundle = ExtensionBundle("SpeedPunk")

import traceback
from AppKit import NSLog

################################################################################################################

speedpunklib = speedpunklib.SpeedPunkLib()

class SpeedPunkTool(EditingTool):

	def becomeActive(self):
		self.speedpunklib = speedpunklib
		self.speedpunklib.tool = self
		self.speedpunklib.Open()

	def becomeInactive(self):
		self.speedpunklib.Close()

	def drawBackground(self, scale):
		try:

			if self.getGlyph() != None:
				self.speedpunklib.UpdateGlyph(self.getGlyph())

		except:
			NSLog('Speed Punk:\n%s' % traceback.format_exc())

	def glyphWindowWillClose(self, a):
		self.speedpunklib.Close()

	def glyphWindowDidOpen(self, a):
		self.speedpunklib.Open()

	def getToolbarTip(self):
		return "Speed Punk"

	def getToolbarIcon(self):
		NSImage = bundle.getResourceImage("toolbar")
		if NSImage:
			return NSImage

installTool(SpeedPunkTool())

