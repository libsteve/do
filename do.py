from optparse import OptionParser

def args():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", default="Makefile", help="specify the file to read from", metavar="FILE")
	parser.add_option("-m", "--machine", dest="machinename", default="glados.cs.rit.edu", help="specify the machine to connect to", metavar="MACHINE")

	(options, args) = parser.parse_args()

def read(filename):
	f = open(filename, 'r')
	if filename == "Makefile" or filename == "makefile":
		readAsMakefile(f)
	else:
		readAsList(f)