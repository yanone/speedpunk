def Interpolate(a, b, p, limit = False):
	u"""\
	Interpolate between values a and b at float position p (0-1)
	Limit: No extrapolation
	"""
	i = a + (b - a) * p
	if limit and i < a:
		return a
	elif limit and i > b:
		return b
	else:
		return i

def Distance(p1, p2):
	u"""\
	Return distance between two points definded as (x, y).
	"""
	
	import math
	
	return math.sqrt( (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 )

def NormalizeMinMax(source_floor, source_ceiling, target_floor, target_ceiling, value):
	u"""\
	Normalize a value from source scale to target scale.
	"""
	
	source_floor, source_ceiling, target_floor, target_ceiling, value = map(float, (source_floor, source_ceiling, target_floor, target_ceiling, value))

	if target_floor == 0:
		return (value - source_floor)/(source_ceiling - source_floor) * target_ceiling
	else:
		return (value - source_floor)/(source_ceiling - source_floor) * (target_ceiling - target_floor) + target_floor

def InterpolateMany(valuelist, p):
	u"""\
	Take a list of values and interpolate them.
	Returns resulting value and the two values that form the floor and ceiling for that value.
	value, floor, ceiling = InterpolateMany((0, 1, 2, 3, 4), 0.0)  # Returns (1.0, 1.0, 2.0)
	value, floor, ceiling = InterpolateMany((0, 1, 2, 3, 4), 0.1)  # Returns (1.4, 1.0, 2.0)
	value, floor, ceiling = InterpolateMany((0, 1, 2, 3, 4), 0.5)  # Returns (3.0, 3.0, 3.0) (floor and ceiling being identical with value, because it's exactly the middle value)
	value, floor, ceiling = InterpolateMany((0, 1, 2, 3, 4), 1.0)  # Returns (5.0, 4.0, 5.0)
	"""
	valuelist = map(float,valuelist)
	p = float(p)

	if len(valuelist) == 1:
		return valuelist[0], valuelist[0], valuelist[0]

	# Return first item
	elif p == 0:
		return valuelist[0], valuelist[0], valuelist[1]

	# Return last item
	elif p == 1.0:
		return valuelist[-1], valuelist[-2], valuelist[-1]

	# Interpolate
	else:
		for i in range(len(valuelist)):

			# p is exactly on one of the values
			if p == i * 1.0 / (len(valuelist)-1):
				return valuelist[i], valuelist[i], valuelist[i]
		
			# Interpolate
			elif i * 1.0 / (len(valuelist)-1) < p < (i+1) * 1.0 / (len(valuelist)-1):

				v1 = valuelist[i]
				v2 = valuelist[i+1]
			
				# Hier liegt der Hase begraben
				_p_floor = (i) * 1.0 / (len(valuelist)-1)
				_p_ceil = _p_floor + 1.0 / (len(valuelist)-1)
				_p = NormalizeMinMax(_p_floor, _p_ceil, 0, 1, p)
			
				return Interpolate(v1, v2, _p), v1, v2
