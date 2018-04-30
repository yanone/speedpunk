






class BaseHTMLTag:

	TYPES = (
	'int',
	'cdata',
	'id',
	'none',
	)

	# name: (type, ([possible value]))
	UNIVERSALATTRIBUTES = (
	'class': ('cdata', None),
	'id': ('id', None),
	'style': ('cdata', None),
	'title': ('cdata', None),
	'dir': ('cdata', ('ltr', 'rtl')),
	'lang': ('cdata', None),
	'onclick': ('cdata', None),
	'ondblclick': ('cdata', None),
	'onmousedown': ('cdata', None),
	'onmouseup': ('cdata', None),
	'onmouseover': ('cdata', None),
	'onmousemove': ('cdata', None),
	'onmouseout': ('cdata', None),
	'onkeypress': ('cdata', None),
	'onkeydown': ('cdata', None),
	'onkeyup': ('cdata', None),
	)

	def __init__(self):
		pass


class A(BaseHTMLTag):
	# name: (type, strict/transitional/frameset, ([possible value]))
	TAGATTRIBUTES = (
	'accesskey': ('cdata', 'stf', None),
	'charset': ('cdata', 'stf', None),
	'coords': ('cdata', 'stf', None),
	'href': ('cdata', 'stf', None),
	'hreflang': ('cdata', 'stf', None),
	'name': ('cdata', 'stf', None),
	'onblur': ('cdata', 'stf', None),
	'onfocus': ('cdata', 'stf', None),
	'rel': ('cdata', 'stf', None),
	'rev': ('cdata', 'stf', None),
	'shape': ('cdata', 'stf', ('rect', 'circle', 'poly', 'default')),
	'tabindex': ('int', 'stf', None),
	'target': ('cdata', 'tf', None),
	'type': ('cdata', 'stf', None),
	)


class ABBR(BaseHTMLTag):
	pass

class ACRONYM(BaseHTMLTag):
	pass

class ADDRESS(BaseHTMLTag):
	pass

class APPLET(BaseHTMLTag):
	# name: (type, strict/transitional/frameset, ([possible value]))
	TAGATTRIBUTES = (
	'align': ('cdata', 'tf', ('top', 'middle', 'bottom', 'left', 'right')),
	'alt': ('cdata', 'tf', None),
	'archive': ('cdata', 'tf', None),
	'code': ('cdata', 'tf', None),
	'codebase': ('cdata', 'tf', None),
	'height': ('cdata', 'tf', None),
	'hspace': ('cdata', 'tf', None),
	'name': ('cdata', 'tf', None),
	'object': ('cdata', 'tf', None),
	'vspace': ('cdata', 'tf', None),
	'width': ('cdata', 'tf', None),
	)

class AREA(BaseHTMLTag):
	# name: (type, strict/transitional/frameset, ([possible value]))
	TAGATTRIBUTES = (
	'alt': ('cdata', 'stf', None),
	'accesskey': ('cdata', 'stf', None),
	'coords': ('cdata', 'stf', None),
	'href': ('cdata', 'stf', None),
	'nohref': ('none', 'stf', None),
	'onblur': ('cdata', 'stf', None),
	'onfocus': ('cdata', 'stf', None),
	'shape': ('cdata', 'stf', ('rect', 'circle', 'poly', 'default')),
	'tabindex': ('int', 'stf', None),
	'target': ('cdata', 'tf', None),
	)

class B(BaseHTMLTag):
	pass



class HTMLGenerator:

	# CONSTANTS
	DOCTYPES = {
		'transitional': '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
		'strict': '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
		}


	def __init__(self, environment = None, title = None, doctype = 'transitional'):

		self.environment = environment
		self.runningID = 0
		
		# HEAD
		self.doctype = self.DOCTYPES[doctype]
		self.title = title
		self.csslinks = []
		self.javascriptlinks = []
		self.metas = []
		self.bodytags = []
		
		# Initialization
		self.Meta('Content-Type', 'text/html; charset=utf-8')
		

	def RunningID(self):
		u"""\
		Just a number, counting up.
		"""
		self.runningID += 1
		return self.runningID

	
	# HEAD TAGS

	def CSSLink(self, target):
		self.csslinks.append( CSSLink(self.environment, target) )
	
	def JSLink(self, target):
		self.javascriptlinks.append( JSLink(self.environment, target) )

	def Meta(self, httpequiv, content):
		self.metas.append( Meta(self.environment, httpequiv, content) )

	# BODY TAGS

	def IMG(self, src, width = None, height = None, alt = None):
		self.bodytags.append( IMG(self.environment, src, width, height, alt) )

	def HTML(self, html):
		self.bodytags.append( HTML(self.environment, html) )


	# META TAGS

	def CheckBox(self, id = None, _class = None, onclick = None, text = None):
		if not id:
			id = "%s_checkbox" % (self.RunningID())
		self.bodytags.append( CheckBox(self.environment, id, _class, onclick, text) )


	# OUTPUT

	def GenerateHTML(self):
		html = []

		for tag in self.bodytags:
			html.append(tag.GenerateHTML())

		return "\n".join(map(str,html))
	
	def GeneratePage(self):
		html = []
		
		# HEAD
		html.append(self.doctype)
		html.append("<html><head>")
		html.append("<title>%s</title>" % (self.title))
		for item in self.metas:
			html.append(item.GenerateHTML())
		for item in self.javascriptlinks:
			html.append(item.GenerateHTML())
		# Missing: JS
		for item in self.csslinks:
			html.append(item.GenerateHTML())
		# Missing: CSS
		html.append("</head>")
		
		# BODY
		html.append("<body>")
		html.append(self.GenerateHTML())
		html.append("</body>")

		html.append("</html>")
		
		return "\n".join(map(str,html))

# HTML Elements

class CSSLink:
	def __init__(self, environment, target):
		self.environment = environment
		self.target = target
	def GenerateHTML(self):
		return '<link href="%s" rel="stylesheet" type="text/css">' % (self.target)

class JSLink:
	def __init__(self, environment, target):
		self.environment = environment
		self.target = target
	def GenerateHTML(self):
		return '<script src="%s" type="text/javascript" charset="utf-8"></script>' % (self.target)

class Meta:
	def __init__(self, environment, httpequiv, content):
		self.environment = environment
		self.httpequiv = httpequiv
		self.content = content
	def GenerateHTML(self):
		return '<meta http-equiv="%s" content="%s">' % (self.httpequiv, self.content)

class IMG:
	def __init__(self, environment, align, alt, border, height, hspace, ismap, longdesc, name, src, usemap, vspace, width, ):
		self.environment = environment
		self.src = src
		self.width = width
		self.height = height
		self.alt = alt
	def GenerateHTML(self):
		html = []
		
		html.append('img src="%s"' % (self.src))
		
		if self.width:
			html.append('width="%s"' % (self.width))

		if self.height:
			html.append('height="%s"' % (self.height))

		if self.alt:
			html.append('alt="%s"' % (self.alt))

		

		return '<%s>' % (" ".join(map(str,html)).strip())
		

class HTML:
	def __init__(self, environment, html):
		self.environment = environment
		self.html = html
	def GenerateHTML(self):
		return self.html

class CheckBox:
	def __init__(self, environment, id, _class, onclick, text):
		self.environment = environment
		self.id = id
		self._class = _class
		self.onclick = onclick
		self.text = text
	def GenerateHTML(self):
		html = []

		html.append('input type="checkbox" id="%s"' % (self.id))

		if self._class:
			html.append('class="%s"' % (self._class))

		if self.onclick:
			html.append('onClick="%s"' % (self.onclick))

		return '<%s> <span style="cursor:default;" onClick="document.getElementById(\'%s\').click();">%s</span>' % (" ".join(map(str,html)).strip(), self.id, self.text)

