def ListPairs(list, num_pairs):
	u"""\
	Return 'num_pairs' amount of elements of list stacked together as lists.
	Example:
	list = ['a', 'b', 'c', 'd', 'e']
	for one, two, three in ListPairs(list, 3):
		print one, two, three
	a b c
	b c d
	c d e
	"""
	returnlist = []
	
	for i in range(len(list) - num_pairs + 1):
		
		singlereturnlist = []
		for j in range(num_pairs):
			singlereturnlist.append(list[i + j])
		
		returnlist.extend([singlereturnlist])
	
	return returnlist


def NaturalSort(l):
	u"""\
	Sort list in natural alpha-numeric order
	file1.jpg, file2.jpg, file10.jpg
	"""

	import re
	convert = lambda text: int(text) if text.isdigit() else text
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
	l.sort( key=alphanum_key )
	return l
