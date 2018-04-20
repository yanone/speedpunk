from fontTools.pens.basePen import BasePen

class CurveSegmentListPen(BasePen):
	u"""\
	Accumulates a list of curve segments in pen.curvesegments
	"""

	lastpoint = None
	lasttype = None
	curvesegments = []

	def moveTo(self, pt):
		self.lastpoint = pt
		self.lasttype = 'move'

	def lineTo(self, pt):
		self.lastpoint = pt
		self.lasttype = 'line'
  
	def curveTo(self, *points):
		self.curvesegments.append((self.lastpoint, points[0], points[1], points[2]))
		self.lastpoint = points[2]
		self.lasttype = 'curve'


class pySVGPen(BasePen):
	u"""\
	Draws onto pySVG path object
	"""

	def __init__(self, glyphSet, x, y, scale, pathobject):
		BasePen.__init__(self, glyphSet)
		self.scale = scale

		self.pathobject = pathobject
		self.x = x
		self.y = y

	def _moveTo(self, (x,y)):
		x = x + self.x
		y = y + self.y	
		self.pathobject.appendMoveToPath(x * self.scale, -y * self.scale, False)

	def _lineTo(self, (x,y)):
		x = x + self.x
		y = y + self.y	
		self.pathobject.appendLineToPath(x * self.scale, -y * self.scale, False)

	def _curveToOne(self, (x1,y1), (x2,y2), (x3,y3)):
		x1 = x1 + self.x	
		x2 = x2 + self.x	
		x3 = x3 + self.x	
		y1 = y1 + self.y	
		y2 = y2 + self.y	
		y3 = y3 + self.y	
		self.pathobject.appendCubicCurveToPath(x1 * self.scale, -y1 * self.scale, x2 * self.scale, -y2 * self.scale, x3 * self.scale, -y3 * self.scale, False)

	def _closePath(self):
		self.pathobject.appendCloseCurve()

	def _endPath(self):
		pass


class NodeBoxPen(BasePen):
	u"""\
	Draws onto NodeBox canvas
	"""

	def __init__(self, glyphSet, x, y, scale, motherobject):
		BasePen.__init__(self, glyphSet)
		self.scale = scale

		self.motherobject = motherobject
		self.x = x
		self.y = -1 * y

	def _moveTo(self, (x,y)):
		x = x + self.x
		y = y + self.y	
		self.motherobject.moveto(x * self.scale, -y * self.scale)

	def _lineTo(self, (x,y)):
		x = x + self.x
		y = y + self.y	
		self.motherobject.lineto(x * self.scale, -y * self.scale)

	def _curveToOne(self, (x1,y1), (x2,y2), (x3,y3)):
		x1 = x1 + self.x	
		x2 = x2 + self.x	
		x3 = x3 + self.x	
		y1 = y1 + self.y	
		y2 = y2 + self.y	
		y3 = y3 + self.y	
		self.motherobject.curveto(x1 * self.scale, -y1 * self.scale, x2 * self.scale, -y2 * self.scale, x3 * self.scale, -y3 * self.scale)

	def _closePath(self):
		self.motherobject.closepath()

	def _endPath(self):
		pass


class BoundingBoxPen(BasePen):
	u"""\
	Calculates BBox. Will be stored in self.ll and self.ur, self.width and self.height
	"""

	def Push(self, x, y):

		# LL

		if not self.ll[0]:
			self.ll[0] = x
		else:
			if x < self.ll[0]:
				self.ll[0] = x

		if not self.ll[1]:
			self.ll[1] = y
		else:
			if y < self.ll[1]:
				self.ll[1] = y

		# UR

		if not self.ur[0]:
			self.ur[0] = x
		else:
			if x > self.ur[0]:
				self.ur[0] = x

		if not self.ur[1]:
			self.ur[1] = y
		else:
			if y > self.ur[1]:
				self.ur[1] = y

		if self.ll and self.ur:
			self.width = self.ur[0] - self.ll[0]
			self.height = self.ur[1] - self.ll[1]


	def __init__(self, glyphSet):
		BasePen.__init__(self, glyphSet)

		self.ll = [None, None]
		self.ur = [None, None]
		self.width = None
		self.height = None

	def _moveTo(self, (x,y)):
		self.Push(x, y)

	def _lineTo(self, (x,y)):
		self.Push(x, y)

	def _curveToOne(self, (x1,y1), (x2,y2), (x3,y3)):
		self.Push(x1, y1)
		self.Push(x2, y2)
		self.Push(x3, y3)
