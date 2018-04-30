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
