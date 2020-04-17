from __future__ import division, print_function, unicode_literals
from vanilla import FloatingWindow, RadioGroup, TextBox, Slider, CheckBox, ImageView

class SpeedPunkPrefWindow(object):

	def __init__(self, parent):
		self.parent = parent
		self.w = FloatingWindow((150, 130), "Speed Punk %s" % VERSION,
								closable = False,
								autosaveName = 'de_yanone_speedPunk_%s.prefWindow' % (environment),
								)
		self.w.illustrationPositionRadioGroup = RadioGroup((10, 10, -10, 40),
								["Outside of glyph", "Outer side of curve"],
								callback=self.radioGroupCallback,
								sizeStyle = "small")

		self.w.curveGainTextBox = TextBox((10, 60, -10, 17), "Gain",
							sizeStyle = "mini")

		self.w.curveGainSlider = Slider((10, 70, -10, 25),
							tickMarkCount=5,
							callback=self.curveGainSliderCallback,
							sizeStyle = "small",
							minValue = curveGain[0],
							maxValue = curveGain[1],
							value = self.parent.getPreference('curveGain'))
		
		self.w.illustrationPositionRadioGroup.set(self.parent.getPreference('illustrationPositionIndex'))

		self.w.faderCheckBox = CheckBox((10, 100, -10, 17), "Fader",
							sizeStyle = "small",
							callback = self.faderCheckBoxCallback)

		self.w.faderSlider = Slider((10, 125, -10, 25),
							sizeStyle = "small",
							minValue = 0,
							maxValue = 1.0,
							value = 1.0,
							callback = self.faderSliderCallback)

		self.w.gradientImage = ImageView((10, 150, -10, 15))
		self.w.histogramImage = ImageView((10, 150, -10, 15))

	def radioGroupCallback(self, sender):
		self.parent.setPreference('illustrationPositionIndex', sender.get())
		self.parent.RefreshView()

	def curveGainSliderCallback(self, sender):
		self.parent.setPreference('curveGain', sender.get())
		self.parent.RefreshView()

	def faderSliderCallback(self, sender):
		self.parent.setPreference('fader', sender.get())
		self.parent.RefreshView()

	def faderCheckBoxCallback(self, sender):
		self.parent.setPreference('useFader', sender.get())
		self.parent.RefreshView()
		if sender.get():
			self.w.faderCheckBox.setPosSize(((10, 105, -10, 17)))
			self.w.resize(150, 175, animate=True)
		else:
			self.w.faderCheckBox.setPosSize(((10, 100, -10, 17)))
			self.w.resize(150, 130, animate=True)
		
