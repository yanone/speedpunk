from ynlib.maths import Interpolate

class Color(object):
	u"""\
	Universal color class.
	Color(hex='FFFFFF') - six digit hex value
	Color(RGB=(0, 127, 255)) - values from 0 to 255
	Color(CMYK=(0, 50, 50, 100)) - values from 0 to 100
	"""
	
	def __init__(self, hex=None, CMYK=None, RGB=None, A = 1.0):
		
		if hex:
			self.min = 0.0
			self.max = 255.0
			self.hex = hex
			self.calcRGB()
			#self.C, self.M, self.Y, self.K = rgb_to_cmyk(self.R, self.G, self.B)
			self.type = 'RGB'
		elif RGB:
			self.min = 0.0
			self.max = 255.0
			self.R, self.G, self.B = map(int, RGB)
			self.calcHex()
			self.type = 'RGB'
		elif CMYK:
			self.min = 0.0
			self.max = 100.0
			self.C, self.M, self.Y, self.K = map(int, CMYK)
			self.type = 'CMYK'
		
		self.A = A

	def lighten(self, value):
		u"""\
		Lighten by float 0..1
		Returns an object in place.
		c = Color(hex='123456').lighten(.2)
		"""
		if self.type == 'RGB':
			other = self.max
			return Color(RGB=(Interpolate(self.R, other, value), Interpolate(self.G, other, value), Interpolate(self.B, other, value)))
		elif self.type == 'CMYK':
			other = self.min
			return Color(CMYK=(Interpolate(self.C, other, value), Interpolate(self.M, other, value), Interpolate(self.Y, other, value), Interpolate(self.K, other, value)))
	
	def darken(self, value):
		u"""\
		Darken by float 0..1
		Returns an object in place.
		c = Color(hex='123456').darken(.2)
		"""
		if self.type == 'RGB':
			other = self.min
			return Color(RGB=(Interpolate(self.R, other, value), Interpolate(self.G, other, value), Interpolate(self.B, other, value)))
		elif self.type == 'CMYK':
			other = self.max
			return Color(CMYK=(Interpolate(self.C, other, value), Interpolate(self.M, other, value), Interpolate(self.Y, other, value), Interpolate(self.K, other, value)))

	def desaturate(self, value):
		u"""\
		Desaturate by float 0..1
		Returns an object in place.
		c = Color(hex='123456').desaturate(.2)
		"""
		if self.type == 'RGB':
			other = (self.R + self.G + self.B) / 3 # Average
			return Color(RGB=(Interpolate(self.R, other, value), Interpolate(self.G, other, value), Interpolate(self.B, other, value)))
		elif self.type == 'CMYK':
			other = (self.C + self.M + self.Y) / 3 # Average
			return Color(CMYK=(Interpolate(self.C, other, value), Interpolate(self.M, other, value), Interpolate(self.Y, other, value), self.K))

#	def __repr__(self):
#		if self.type == 'RGB':
#			return "<yn RGB Color %s %s %s>" % (self.R, self.G, self.B)
#		else:
#			return "<yn CMYK Color %s %s %s %s>" % (self.C, self.M, self.Y, self.K)

	def calcRGB(self):
		self.R = int(self.hex[0:2], 16)
		self.G = int(self.hex[2:4], 16)
		self.B = int(self.hex[4:6], 16)

	def calcHex(self):
		u"""\
		Convert float (R, G, B) tuple to RRGGBB hex value (without #).
		"""
		import string
		self.hex = (string.zfill(str(hex(self.R)[2:]), 2) + string.zfill(str(hex(self.G)[2:]), 2) + string.zfill(str(hex(self.B)[2:]), 2)).upper()


# Conversion from http://stackoverflow.com/questions/14088375/how-can-i-convert-rgb-to-cmyk-and-vice-versa-in-python 
cmyk_scale = 100
def rgb_to_cmyk(r,g,b):
	if (r == 0) and (g == 0) and (b == 0):
		# black
		return 0, 0, 0, cmyk_scale

	# rgb [0,255] -> cmy [0,1]
	c = 1 - r / 255.
	m = 1 - g / 255.
	y = 1 - b / 255.

	# extract out k [0,1]
	min_cmy = min(c, m, y)
	c = (c - min_cmy) / (1 - min_cmy)
	m = (m - min_cmy) / (1 - min_cmy)
	y = (y - min_cmy) / (1 - min_cmy)
	k = min_cmy

	# rescale to the range [0,cmyk_scale]
	return c*cmyk_scale, m*cmyk_scale, y*cmyk_scale, k*cmyk_scale


def InterpolateHexColorList(colors, p):
	u"""\
	Interpolate between list of hex RRGGBB values at float position p (0-1)
	Returns float list (R, G, B)
	"""

	from ynlib.maths import Interpolate

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

def InterpolateColor(color1, color2, p):
	u"""\
	Interpolate between two colors as float lists (R, G, B) at float position p (0-1)
	Returns float list (R, G, B)
	"""

	from ynlib.maths import Interpolate

	R = Interpolate(color1[0], color2[0], p) 
	G = Interpolate(color1[1], color2[1], p) 
	B = Interpolate(color1[2], color2[2], p) 
	return (R, G, B)


def DesaturateColor(color, p):
	u"""\
	Desature a color as a float list (R, G, B) at float position p (0-1).
	Returns float list (R, G, B)
	"""

	from ynlib.maths import Interpolate

	R = color[0]
	G = color[1]
	B = color[2]
	
	average = (R + G + B) / 3
	R = Interpolate(R, average, p) 
	G = Interpolate(G, average, p) 
	B = Interpolate(B, average, p) 

	return (R, G, B)

def DarkenColor(color, p):
	u"""\
	Darken a color as a float list (R, G, B) at float position p (0-1).
	Returns float list (R, G, B)
	"""

	from ynlib.maths import Interpolate

	R = color[0]
	G = color[1]
	B = color[2]
	
	R = Interpolate(R, 0, p) 
	G = Interpolate(G, 0, p) 
	B = Interpolate(B, 0, p) 

	return (R, G, B)

def BrightenColor(color, p):
	u"""\
	Brighten a color as a float list (R, G, B) at float position p (0-1).
	Returns float list (R, G, B)
	"""

	from ynlib.maths import Interpolate

	R = color[0]
	G = color[1]
	B = color[2]
	
	R = Interpolate(R, 1, p) 
	G = Interpolate(G, 1, p) 
	B = Interpolate(B, 1, p) 

	return (R, G, B)

def RGBToInt(R, G, B):
	u"""\
	Convert color from RGB (0..255) to integer value (0..16M)
	"""
	return int(long(R) | (long(G) << 8) | (long(B) << 16))

def HextoRGB(hexstring):
	u"""\
	Convert RRGGBB hex value (without #) to float (R, G, B) tuple.
	"""
	return (int(hexstring[0:2], 16) / 255.0, int(hexstring[2:4], 16) / 255.0, int(hexstring[4:6], 16) / 255.0)

def RGBtoHex(color):
	u"""\
	Convert float (R, G, B) tuple to RRGGBB hex value (without #).
	"""
	import string
	
	return string.zfill(str(hex(int(color[0] * 255))[2:]), 2) + string.zfill(str(hex(int(color[1] * 255))[2:]), 2) + string.zfill(str(hex(int(color[2] * 255))[2:]), 2)

def Multiply255(color):
	u"""\
	Convert float (R, G, B) tuple to 0-255 (R, G, B) tuple.
	"""
	return (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

