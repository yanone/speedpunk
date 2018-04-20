# -*- coding: utf-8 -*-

from ynlib.maths import NormalizeMinMax
import math

class Histogram(object):
	def __init__(self):

		self.xMin = None
		self.xMax = None
		self.yMin = 0
		self.yMax = 0
		
		self.values = {}
	
	def addValue(self, x, addition = 1):
		if self.values.has_key(x):
			self.values[x] += addition
		else:
			self.values[x] = addition
		
		if x < self.xMin or not self.xMin:
			self.xMin = x
		if x > self.xMax or not self.xMax:
			self.xMax = x

		if self.values[x] < self.yMin:
			self.yMin = self.values[x]
		if self.values[x] > self.yMax:
			self.yMax = self.values[x]

	def outputMatrix(self, xMin, xMax, yMin, yMax, scaleYMax = None):
		
		width = xMax - xMin
		height = yMax - yMin
		
		matrix = ('_' * width + '\n') * height
		
		for x in self.values.keys():
			for y in range(self.values[x]):
				
				if not scaleYMax:
					scaleYMax = yMax
				
				_y = int(NormalizeMinMax(self.yMin, self.yMax, yMin, scaleYMax, y)) - 1
				
				pos = (width + 1) * (height - (_y - yMin + 1) - 1) + x
				
				matrix = matrix[:pos] + '#' + matrix[pos+1:]
		
		return matrix[:len(matrix)-1] # remove last line break
