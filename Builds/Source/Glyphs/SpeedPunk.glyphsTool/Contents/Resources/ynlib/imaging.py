def InterpolateImageFGColorOnTop(bg, fg, fgcolor):
	u"""\
	Interpolate PIL image in the way that RRGGBB fgcolor stays and the rest is interpolated against it.
	fg needs to be an image with values between black and fgcolor.
	"""
	
	from ynlib.maths import Interpolate
	from ynlib.colors import HextoRGB, Multiply255
	from PIL import Image
	
	new = Image.new("RGB", bg.size, "#000000")
	bg = bg.convert("RGB")
	fg = fg.convert("RGB")

	bgpix = bg.load()
	fgpix = fg.load()
	newpix = new.load()

	fgcolor = Multiply255(HextoRGB(fgcolor))

	for x in range(bg.size[0]):
		for y in range(bg.size[1]):
		
			# color bands
			for i in range(3):
		
		
				# abstand vom fg-pixel zum fgcolor
				fgdelta = fgcolor[i] - fgpix[x, y][i]
				
				try:
					p = float((fgcolor[i] - fgdelta)) / float(fgcolor[i])
				except:
					p = 1.0
			
				pixel = list(newpix[x, y])
				pixel[i] = int(Interpolate(bgpix[x, y][i], fgcolor[i], p))
						
				newpix[x, y] = tuple(pixel)
	
	return new


def imageFileDimensions(path):

	from ynlib.system import Execute
	import re
	
	identify = Execute('identify -ping "%s"' % path)
	m = re.match(r".*?(\d+)x(\d+).*?", identify)
	return (int(m.group(1)), int(m.group(2)))
