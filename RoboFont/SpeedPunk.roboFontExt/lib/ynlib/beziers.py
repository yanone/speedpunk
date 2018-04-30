class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	
	def __add__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(self.x + other.x, self.y + other.y)

	__radd__ = __add__
	
	def __sub__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(self.x - other.x, self.y - other.y)

	def __rsub__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(other.x - self.x, other.y - self.y)

	def __mul__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(self.x * other.x, self.y * other.y)
	
	__rmul__ = __mul__

	def __div__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(self.x / other.x, self.y / other.y)

	def __rdiv__(self, other):
		if isinstance(other, int) or isinstance(other, float):
			other = Point(other, other)
		return Point(other.x / self.x, other.y / self.y)

	def __abs__(self):
		import math
		return math.sqrt(self.x**2 + self.y**2)


	def __neg__(self):
		return Point(-self.x, -self.y)

#	def __cmp__(self, other):
#		c = hash(other) - hash(self)
#		if not isinstance(c, int):
#			c = int(-1)
#		return c

	def __eq__(self, other):
	    return (self.x, self.y) == (other.x, other.y)

	def __ne__(self, other):
	    return (self.x, self.y) != (other.x, other.y)
	
	def __hash__(self):
		return hash((self.x, self.y))

	def __repr__(self):
		return '<Point %s %s>' % (self.x, self.y)


def solveCubicBezier(p1, p2, p3, p4, t):
	u"""\
	Solve cubic Bezier equation and 1st and 2nd derivative.
	Returns position of on-curve point p1234, and vector of 1st and 2nd derivative.
	"""
	a = -p1 + 3.0 * p2 - 3.0 * p3 + p4
	b = 3.0 * p1 - 6.0 * p2 + 3.0 * p3
	c = -3.0 * p1 + 3.0 * p2
	d = p1

	r = a*t**3 + b*t**2 + c*t + d
	r1 = 3*a*t**2 + 2*b*t + c
	r2 = 6*a*t + 2*b
	
	return r, r1, r2

def solveCubicBezierCurvature(r, r1, r2):
	u"""\
	Calc curvature using cubic Bezier equation and 1st and 2nd derivative.
	"""
	return (r1.x * r2.y - r1.y * r2.x) / (r1.x**2 + r1.y**2)**1.5


def _SplitCubicAtT(p1, p2, p3, p4, t):
	u"""\
	Split cubic Beziers curve at relative value t, return the two resulting segments.
	"""
	
	from ynlib.maths import Interpolate
	
	p12 = (Interpolate(p1[0], p2[0], t), Interpolate(p1[1], p2[1], t))
	p23 = (Interpolate(p2[0], p3[0], t), Interpolate(p2[1], p3[1], t))
	p34 = (Interpolate(p3[0], p4[0], t), Interpolate(p3[1], p4[1], t))

	p123 = (Interpolate(p12[0], p23[0], t), Interpolate(p12[1], p23[1], t))
	p234 = (Interpolate(p23[0], p34[0], t), Interpolate(p23[1], p34[1], t))

	p1234 = (Interpolate(p123[0], p234[0], t), Interpolate(p123[1], p234[1], t))

	return (p1, p12, p123, p1234), (p1234, p234, p34, p4)

def SplitCubicAtT(p1, p2, p3, p4, t):
	u"""\
	Split cubic Beziers curve at relative value t, return the two resulting segments.
	"""
	
	from ynlib.maths import Interpolate
	
	p12 = Point(Interpolate(p1.x, p2.x, t), Interpolate(p1.y, p2.y, t))
	p23 = Point(Interpolate(p2.x, p3.x, t), Interpolate(p2.y, p3.y, t))
	p34 = Point(Interpolate(p3.x, p4.x, t), Interpolate(p3.y, p4.y, t))

	p123 = Point(Interpolate(p12.x, p23.x, t), Interpolate(p12.y, p23.y, t))
	p234 = Point(Interpolate(p23.x, p34.x, t), Interpolate(p23.y, p34.y, t))

	p1234 = Point(Interpolate(p123.x, p234.x, t), Interpolate(p123.y, p234.y, t))

	return (p1, p12, p123, p1234), (p1234, p234, p34, p4)


def GuessSmoothSegmentConnection(s1, s2):
	u"""\
	Returns True if the two segments are connected and their inner BCPs align (within a certain threshold).
	"""

	import math
	from ynlib.geometry import SmallerAngleBetweenLines

	thresholdangle = 3
	
	if s1[3] == s2[0] and math.fabs(SmallerAngleBetweenLines(s1[2], s1[3], s2[0], s2[1])) < thresholdangle:
		return True
	else:
		return False

def CurveSegments(glyph):
	u"""\
	Returns a list of consecutive curve segments of RGlyph object using ynlib.pens.CurveSegmentListPen
	"""

	from ynlib.pens import CurveSegmentListPen
	
	pen = CurveSegmentListPen({})
	pen.curvesegments = []
	glyph.draw(pen)

	return pen.curvesegments

def ConsecutiveCurveSegments(segments, smooth = False):
	u"""\
	Turns a flat list of curve segments into lists of lists of consecutive curve segments.
	If 'smooth' is set to True, segments will only be connected if their connection is guessed to be smooth.
	"""
	
	newsegments = []
	tempcurvesegments = []

	for i, segment in enumerate(segments):

		if i == 0:
			tempcurvesegments.append(segment)
				
		if i >= 1:
			prevsegment = segments[i - 1]
			
			if smooth == True and GuessSmoothSegmentConnection(prevsegment, segment): # is connected and smooth
				tempcurvesegments.append(segment)
				
			elif smooth == False and prevsegment[3] == segment[0]: # is connected
				tempcurvesegments.append(segment)

			else:
				newsegments.extend([tempcurvesegments])
				tempcurvesegments = []
				tempcurvesegments.append(segment)

	newsegments.extend([tempcurvesegments])
	return newsegments
	

def SameLengthSegments(segment, distance, precision, firstpoint = None):
	u"""\
	Finds points on a curve segment with equal distance (approximated through binary search, with given precision).

	If firstpoint is given, that would in most cases be the second last calculated point of the previous segment
	(to avoid gaps between smooth connection segments), this point is used as the starting point instead of p1.
	The distance from firstpoint to p1 should then be less than 'distance'.
	
	Returns a list with calculated points and the position of the last calculated point.
	"""
	
	from ynlib.maths import Distance
	from ynlib.beziers import SplitCubicAtT

	points = []
	p1, p2, p3, p4 = segment
	l = distance
	t = None

	segments = SplitCubicAtT(p1, p2, p3, p4, .5)

	# Use firstpoint	
	firstrun = True
	if firstrun and firstpoint != None:
		d = Distance(firstpoint, segments[0][3])
	else:
		d = Distance(p1, segments[0][3])

	count = 0

	while Distance(segments[1][0], p4) > l:

		min = 0
		max = 1
#		if t != None:
#			min = t
		t = min + (max - min) / 2.0

		segments = SplitCubicAtT(p1, p2, p3, p4, t)
		if firstrun and firstpoint != None:
			d = Distance(firstpoint, segments[0][3])
		else:
			d = Distance(p1, segments[0][3])

		# Binary search
		while (d - l) > precision or (d - l) < (precision * -1):
			
			if (d-l) > 0:
				max = t
			elif (d-l) < 0:
				min = t
			t = min + (max - min) / 2.0

			segments = SplitCubicAtT(p1, p2, p3, p4, t)

			# Use last point of previous curve as first point
			if firstrun and firstpoint != None:
				d = Distance(firstpoint, segments[0][3])
			else:
				d = Distance(segments[0][0], segments[0][3])
				
			count += 1
			
		p1 = segments[1][0]
		p2 = segments[1][1]
		p3 = segments[1][2]

		points.append(segments[0][3])
		firstrun = False
		

	# List of points excluding, last point
	return points, segment[3], count

