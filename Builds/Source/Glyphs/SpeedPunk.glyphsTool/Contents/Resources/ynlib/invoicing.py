class EUInvoicing(object):
	def __init__(self, homeCountry, EUwithVATdict, clientCountry, clientVATID, netto):
		self.homeCountry = homeCountry
		self.EUwithVATdict = EUwithVATdict
		self.clientCountry = clientCountry
		self.clientVATID = clientVATID or None

		self.netto = netto
		self.tax = 0
		self.brutto = netto
		self.EUprivate = False
		self.reverseCharge = False
		self.taxPercentage = 0
		
		# DE
		if self.clientCountry == self.homeCountry:
			self.tax = self.netto * self.taxPercent(self.clientCountry)
			self.brutto = self.netto + self.tax
			self.taxPercentage = self.EUwithVATdict[self.clientCountry]

		# EU, private
		elif self.clientCountry in self.EUwithVATdict.keys() and self.clientVATID == None:
			self.tax = self.netto * self.taxPercent(self.clientCountry)
			self.brutto = self.netto + self.tax
			self.taxPercentage = self.EUwithVATdict[self.clientCountry]
			self.EUprivate = True

		# EU, company
		elif self.clientCountry in self.EUwithVATdict.keys() and self.clientVATID != None:
			self.reverseCharge = True

		# Outside EU
		else:
			pass

	def taxPercent(self, country):
		return int(self.EUwithVATdict[country]) / 100.0

def test():

	EUwithVATdict = {
		'DE': 19,
		'FR': 20,
		'CZ': 21,
		}

	i = EUInvoicing(
		homeCountry = 'DE',
		EUwithVATdict = EUwithVATdict,
		clientCountry = 'DE',
		clientVATID = 'DE123456789',
		netto = 100.0
		)

	print i.netto
	print i.tax
	print i.brutto
	print i.reverseCharge

if __name__ == '__main__':
	test()