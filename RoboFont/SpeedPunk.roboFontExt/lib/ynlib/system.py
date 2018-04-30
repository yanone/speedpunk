def Execute(command):
	u"""\
	Execute system command, return output.
	"""

	import sys, os

	if sys.version.startswith("2.3"):

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
