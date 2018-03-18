# -*- coding: utf-8 -*-
# encoding=utf8  

from ynlib.system import Execute
import os, sys
reload(sys)  
sys.setdefaultencoding('utf-8')
import PyPDF2



class PDF(object):

	def __init__(self, path):
		self.path = path
		self.pypdf = PyPDF2.PdfFileReader(self.path)
		self.amountPages = len(self.pypdf.pages)

		architecture = Execute('uname -a')

		if '86_64' in architecture:
			bit = '64'
		else:
			bit = '32'
		
		osVersion = None
		if 'Darwin' in architecture:
			osVersion = 'mac'
		elif 'Linux' in architecture:
			osVersion = 'linux'

		self.binary = os.path.join(os.path.dirname(__file__), 'pdftotext_%s%s' % (osVersion, bit))

	def pageText(self, pageNumber):


		import tempfile
		tempFolder = tempfile.gettempdir()

		tempTextFile = os.path.join(tempFolder, 'pdf.txt')
		if os.path.exists(tempTextFile):
			os.remove(tempTextFile)

		call = '"%s" -f %s -l %s -enc UTF-8 -table "%s" "%s"' % (self.binary, pageNumber + 1, pageNumber + 1, self.path, tempTextFile)
		Execute(call)

		text = open(tempTextFile, 'r').read()

		if os.path.exists(tempTextFile):
			os.remove(tempTextFile)

		return text

	def savePagesToFile(self, path, pageNumbers):
		outPDF = PyPDF2.PdfFileWriter()

		if type(pageNumbers) == int:
			pageNumbers = [pageNumbers]

		for pageNumber in pageNumbers:
			outPDF.addPage(self.pypdf.getPage(pageNumber))
			output = open(path, 'wb')
			outPDF.write(output)
			output.close()



if __name__ == '__main__':
	pdf = PDF('/Users/yanone/Downloads/2017-10_105357_17PN273744.pdf')
#	pdf = PDF('/Users/yanone/Downloads/_Users_yanone_Downloads_Rechnung 201771565 V1.pdf')
#	pdf = PDF('/Users/yanone/Dropbox/Juicie Cafe/Lohnabrechnungen/2017/10-17/Formular plus.pdf')

#	pdf.savePagesToFile('/Users/yanone/Downloads/Lohnabrechnung.pdf', [0, 1])

#	txt = open('/Users/yanone/Downloads/Lohnabrechnung.txt', 'w')
#	txt.write(pdf.pageText(0))
#	txt.close()

	print pdf.pageText(0) 

	print 'end'