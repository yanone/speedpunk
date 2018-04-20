import rtmidi, time

import threading
class midiListener(threading.Thread): 
	def __init__(self, midi): 
		threading.Thread.__init__(self) 
		self.midi = midi
 
	def run(self): 
		self.midi.midiin.openPort(0)
		while True:
			time.sleep(.1)
		self.midi.midiin.closePort()

	def stop(self):
		self._Thread__stop()



class MidiWithCallBack:
	def __init__(self):
		
		# SETUP MIDI
		self.midiin = rtmidi.RtMidiIn()
		
		self.functions = {}
		
		# Start listening
		self.midiin.setCallback(self.callFunction)

		self.listener = midiListener(self)

	def startListening(self):
		'''Start listenting'''


		self.listener.start()


#		self.midiin.openPort(0)
#		while True:
#			time.sleep(.1)
#		self.midiin.closePort()

	def stop(self):
		self.listener.stop()

	def registerFunction(self, function, channel = None):
		'''Map function to MIDI channels'''
		
		if not channel:
			channel = -1
		
		self.functions[channel] = function

	def callFunction(self, midi):
		'''Call registered functions'''
		
		if midi.isNoteOn():
			channel = midi.getMidiNoteName(midi.getNoteNumber())
			value = midi.getVelocity()
		elif midi.isNoteOff():
			channel = midi.getMidiNoteName(midi.getNoteNumber())
			value = 0
		elif midi.isController():
			channel = midi.getControllerNumber()
			value = midi.getControllerValue()
		
		# Default mapping
		if not self.functions.has_key(channel):
			channel = -1

		# Call
		if self.functions.has_key(channel):
			f = self.functions[channel]
			#print f
			#eval(f.__name__ + '(midi)')
			f(channel, value)
