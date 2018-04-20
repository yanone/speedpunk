#!/usr/bin/env python
# encoding: utf-8

##########################################################################################
#
#	SpeedPunk 1.01
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

import objc
from AppKit import *
from Foundation import *
import sys, os, re

import speedpunk.speedpunklib

speedpunklib = speedpunk.speedpunklib.SpeedPunkLib()

class GlyphsAppSpeedPunkTool (GSToolSelect):

	
	def init(self):
		Bundle = NSBundle.bundleForClass_(NSClassFromString(self.className()));
		BundlePath = Bundle.pathForResource_ofType_("toolbar", "pdf")
		self.tool_bar_image = NSImage.alloc().initWithContentsOfFile_( BundlePath )
		self.tool_bar_image.setTemplate_(True)
		
		self.speedpunklib = speedpunklib
		self.speedpunklib.tool = self

		return self

	
	def title(self):
		return "Speed Punk"
		
	def willActivate(self):
		self.speedpunklib.Open()
		super(GlyphsAppSpeedPunkTool, self).willActivate()

	def willDeactivate(self):
		self.speedpunklib.Close()
		super(GlyphsAppSpeedPunkTool, self).willDeactivate()
		
	def interfaceVersion(self):
		return 1
	
	def groupID(self):
		'''determines the position in the toolbar '''
		return 100
	
 	def trigger(self):
		'''The key to select the tool with keyboard'''
		return "x"
	
	def toolBarIcon(self):
		'''return a instance of NSImage that represents the tool bar icon'''
		return self.tool_bar_image

	def drawBackgroundForLayer_(self, Layer):
		self.speedpunklib.UpdateGlyph(Layer)

	# Prevent disappearing of illustration upon press of Command key
	def willSelectTempTool_(self, TempTool):
		if TempTool.isKindOfClass_(NSClassFromString("GSToolSelect")):
			return False
		else:
			return True
