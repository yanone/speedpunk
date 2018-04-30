def Interpolate(a, b, p):
	u"""\
	Interpolate between values a and b at float position p (0-1)
	"""
	return a + (b - a) * p


def Distance(p1, p2):
	u"""\
	Return distance between two points definded as (x, y).
	"""
	
	import math
	
	return math.sqrt( (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 )
