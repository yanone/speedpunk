#serial is PySerial, the serial port software for Python
import serial





#setup the dmx
#char 126 is 7E in hex. It's used to start all DMX512 commands
DMXOPEN=chr(126)

#char 231 is E7 in hex. It's used to close all DMX512 commands
DMXCLOSE=chr(231)

#I named the "output only send dmx packet request" DMXINTENSITY as I don't have
#any moving fixtures. Char 6 is the label , I don't know what Char 1 and Char 2 mean
#but my sniffer log showed those values always to be the same so I guess it's good enough. 
DMXINTENSITY=chr(6)+chr(1)+chr(2)

#this code seems to initialize the communications. Char 3 is a request for the controller's
#parameters. I didn't bother reading that data, I'm just assuming it's an init string.
DMXINIT1= chr(03)+chr(02)+chr(0)+chr(0)+chr(0)

#likewise, char 10 requests the serial number of the unit. I'm not receiving it or using it
#but the other softwares I tested did. You might want to.
DMXINIT2= chr(10)+chr(02)+chr(0)+chr(0)+chr(0)

#open serial port 4. This is where the USB virtual port hangs on my machine. You
#might need to change this number. Find out what com port your DMX controller is on
#and subtract 1, the ports are numbered 0-3 instead of 1-4
#ser=serial.Serial()

#this writes the initialization codes to the DMX
#ser.write( DMXOPEN+DMXINIT1+DMXCLOSE)
#ser.write( DMXOPEN+DMXINIT2+DMXCLOSE)

# this sets up an array of 513 bytes, the first item in the array ( dmxdata[0] ) is the previously
#mentioned spacer byte following the header. This makes the array math more obvious


#senddmx accepts the 513 byte long data string to keep the state of all the channels
# the channel number and the value for that channel
#senddmx writes to the serial port then returns the modified 513 byte array
 
# to change a light on channel 1 to full bright
#a = senddmx(dmxdata,1,0)
#a = senddmx(dmxdata,2,0)
# to dim it to half
#dmxdata= senddmx(dmxdata,1,128)
# to black it out
#dmxdata= senddmx(dmxdata,1,0)

class DMX(object):
	def __init__(self, name, initValues = {}):
		self.name = name
		self.ser=serial.Serial(self.name)
		self.dmxdata = [chr(0)]*513
		
		# Set init values
		for channel in initValues.keys():
			self.setValue(channel, initValues[channel])
		
		self.ser.write( DMXOPEN+DMXINIT1+DMXCLOSE)
		self.ser.write( DMXOPEN+DMXINIT2+DMXCLOSE)

	def setValue(self, channel, intensity):
		# because the spacer bit is [0], the channel number is the array item number
		# set the channel number to the proper value
		self.dmxdata[channel]=chr(int(intensity))
		
	def send(self):
		# join turns the array data into a string we can send down the DMX
		sdata=''.join(self.dmxdata)
		# write the data to the serial port, this sends the data to your fixture
		self.ser.write(DMXOPEN+DMXINTENSITY+sdata+DMXCLOSE)
		# return the data with the new value in place

	def zeroAllChannels(self):
		self.dmxdata=[chr(0)]*513
		sdata=''.join(self.dmxdata)
		self.ser.write(DMXOPEN+DMXINTENSITY+sdata+DMXCLOSE)
