def RotatePointAroundPoint(c, p, a):
	u"""Rotate point p around center point c with a degrees of angle."""

	import math
	
	p2 = Point()

	p2.x = math.cos(math.radians(a)) * (p.x-c.x) - math.sin(math.radians(a)) * (p.y-c.y) + c.x
	p2.y = math.sin(math.radians(a)) * (p.x-c.x) + math.cos(math.radians(a)) * (p.y-c.y) + c.y

	return p2


def SmallerAngleBetweenLines(p1, p2, p3, p4):
	u"""Calculate the angle between the line from p1 to p2
	and the line from p3 to p4.
	It always returns the smaller angle of a full circle (360 degrees)."""
	
	import math

	x1 = p1.x - p2.x
	y1 = p1.y - p2.y
	x2 = p3.x - p4.x
	y2 = p3.y - p4.y

	angle1 = math.atan2(y1, x1)
	angle2 = math.atan2(y2, x2)
	
	angle = math.degrees(angle2-angle1)

	if angle > 180:
		angle = angle - 360
	elif angle < -180:
		angle = angle + 360
	return angle


def clockwise(p1, p2, p3):
	u"""\
	Returns True for clockwise, False for counterclockwise
	"""
	v1 = p2 - p1
	v2 = p3 - p2
	c = (v2.x * v1.y) - (v1.x * v2.y)
	if c > 0:
		return True
	else:
		return False


def pointInTriangle(p, t1, t2, t3):
	u"""\
	True if point p is in triangle t.
	"""
	return (clockwise(p, t1, t2) and clockwise(p, t2, t3) and clockwise(p, t3, t1)) or (not clockwise(p, t1, t2) and not clockwise(p, t2, t3) and not clockwise(p, t3, t1))


def triangulate(polyline):
	u"""\
	Returns list of triangles in tuples of three points, calculated using poly2tri (Google Code).
	"""
	import p2t
	from ynlib.beziers import Point

	# Convert into p2t Points
	for p in polyline:
		p = p2t.Point(p.x, p.y)
	
	cdt = p2t.CDT(polyline)
	p2ttriangles = cdt.triangulate()
	
	triangles = []
	for t in p2ttriangles:
		triangles.append( (Point(t.a.x, t.a.y), Point(t.b.x, t.b.y), Point(t.c.x, t.c.y)) )

	return triangles
		