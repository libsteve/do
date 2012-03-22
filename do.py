from optparse import OptionParser

def get_args():
	parser = OptionParser()
	parser.add_option("-f", "--file", dest="filename", default="", help="specify the file to read from")
	parser.add_option("-m", "--machine", dest="machine", default="glados.cs.rit.edu", help="specify the machine to connect to")
	parser.add_option("-u", "--user", dest="username", default="", help="specify the user")
	
	(options, args) = parser.parse_args()
	return (options, args)

from reader import *

def main():
	(options, args) = get_args()
	filename = options.filename
	filename = find_file(filename)
	if filename != None:
		(sections, data) = parse_file(filename)
		(machine, username, password) = get_proper_connection_values(data, options)
		
	else:
		print("No File Found\n")
		return

def get_password():
	import getpass
	return getpass.getpass()

import sys

def get_proper_connection_values(data, options):
	def x_or_y(x, y):
		if x == "": return y
		else: return x
	machine = x_or_y(options.machine, data.machine)
	username = x_or_y(options.username, data.username)
	if machine == "":
		print("Machine: "),
		machine = raw_input()
	if username == "":
		print("Username:"),
		username = raw_input()
	password = get_password()
	return (machine, username, password)

main()
