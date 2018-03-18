#!/usr/bin/env python
# encoding: utf-8

##########################################################################################
#
#	SpeedPunk %%VERSION%%
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

from GlyphsApp.plugins import SelectTool


import speedpunk.speedpunklib
speedpunklib = speedpunk.speedpunklib.SpeedPunkLib()


class GlyphsAppSpeedPunkTool(SelectTool):
	
	def settings(self):
		self.name = 'Speed Punk'
		self.keyboardShortcut = 'x'

	def start(self):
		self.speedpunklib = speedpunklib
		self.speedpunklib.tool = self

	def activate(self):
		self.speedpunklib.Open()

	def deactivate(self):
		self.speedpunklib.Close()

	def background(self, layer):
		self.speedpunklib.UpdateGlyph(layer)

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__