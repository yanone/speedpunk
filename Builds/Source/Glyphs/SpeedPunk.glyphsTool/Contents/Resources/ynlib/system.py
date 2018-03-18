import platform

def Execute(command):
	u"""\
	Execute system command, return output.
	"""

	import sys, os, platform

	if sys.version.startswith("2.3") or platform.system() == "Windows":

		p = os.popen(command, "r")
		response = p.read()
		p.close()
		return response


	else:

		import subprocess

		process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, close_fds=True)
		os.waitpid(process.pid, 0)
		response = process.stdout.read().strip()
		process.stdout.close()
		return response

def Stamina():
	u"""\
	Calculate system power as integer using by mulitplying number of active CPUs with clock speed.
	"""
	from ynlib.system import Execute
	return int(Execute('sysctl hw.activecpu').split(' ')[-1]) * int(Execute('sysctl hw.cpufrequency').split(' ')[-1])

def MD5OfFile(filename):
	u"""\
	Calculate hex MD5 sum of file.
	"""
	import hashlib
	md5 = hashlib.md5()
	with open(filename,'rb') as f: 
		for chunk in iter(lambda: f.read(128*md5.block_size), b''): 
			 md5.update(chunk)
	return md5.hexdigest()





import os
import sys    
import termios
import fcntl
import time

def GetChr(waitMaximalSeconds = None):
	u"""\
	Wait for single keyboard press and return character
	"""

	firstCallTime = time.time()

	fd = sys.stdin.fileno()

	oldterm = termios.tcgetattr(fd)
	newattr = termios.tcgetattr(fd)
	newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
	termios.tcsetattr(fd, termios.TCSANOW, newattr)

	oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
	fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

	try:
		while 1:
			try:
				c = sys.stdin.read(1)
				break
			except IOError: pass
			time.sleep(.1)
			
			# Return if waitMaximalSeconds is reached:
			if waitMaximalSeconds > 0:
				if time.time() > firstCallTime + waitMaximalSeconds:
					return None
			
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
	return c


def MachineName():
	if platform.system() == 'Linux':
		
		cpu = ''
		itemsUsed = []
		procinfo = Execute('cat /proc/cpuinfo')

		for line in procinfo.split('\n'):
			if ':' in line:
				k, v = line.split(':')[:2]
				if k.strip() == 'model name' and not k in itemsUsed:
					cpu += v.strip()
					itemsUsed.append(k)
		return '%s %s with %s' % (Execute('cat /sys/devices/virtual/dmi/id/sys_vendor'), Execute('cat /sys/devices/virtual/dmi/id/product_name'), cpu)

	elif platform.system() == 'Darwin':
		import plistlib
		data = plistlib.readPlistFromString(Execute('system_profiler -xml SPHardwareDataType'))
		return 'Apple %s (%s) with %s %s, %s memory' % (data[0]['_items'][0]['machine_name'], data[0]['_items'][0]['machine_model'], data[0]['_items'][0]['cpu_type'], data[0]['_items'][0]['current_processor_speed'], data[0]['_items'][0]['physical_memory'])

if __name__ == '__main__':
	print MachineName()
	# print MachineName()[0]['_items']
	# print MachineName()[0]['_items'][0]['machine_name']
