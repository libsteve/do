from optparse import OptionParser

def args():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", default="", help="specify the file to read from")
	parser.add_option("-m", "--machine", dest="machine", default="glados.cs.rit.edu", help="specify the machine to connect to")
	parser.add_option("-u", "--user", dest="username", default="", help="specify the user")
	parser.add_option("-p", "--password", dest="password", default="", help="specify the password")

	(options, args) = parser.parse_args()
	return (options, args)

def main():
	(options, args) = args()
	filename = options.filename
	machine = options.machine
	username = options.username
	password = options.password