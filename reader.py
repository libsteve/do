import string


class section:
	pass


class project:
	pass


class session:
	pass


class data:
	pass


def _mk_section(name):
	x = section()
	x.name = name
	x.projects = []
	return x


def _mk_project(name, section):
	x = project()
	x.name = name
	section.projects += [x]
	x.section = section
	x.files = []
	return x


def _mk_data():
	x = data()
	x.username = ""
	x.machine = ""
	return x


def _mk_session():
	x = session()
	x.current_section = None
	x.current_project = None
	x.sections = []
	x.do_declaired = False
	x.data = _mk_data()
	return x

######
## here are commands

def _make_section(sess, name):
	sess.current_section = _mk_section(name)
	sess.sections += [sess.current_section]


def _set_username(sess, name):
	sess.data.username = name


def _set_machine(sess, name):
	sess.data.machine = name


_one_arg_commands = {
	'class':lambda sess, x: _make_section(sess, x), 
	'username':lambda sess, x: _set_username(sess, x),
	'machine':lambda sess, x: _set_machine(sess, x)
}

def _set_do_declaired(sess, val):
	sess.do_declaired = val

_no_arg_commands = {
	'enddo':lambda sess: _set_do_declaired(sess, False),
	'dofile':lambda sess: _set_do_declaired(sess, True)
}

## commands end
######


def find_file(filename):
	if filename == "":
		default_files = ['dofile', 'dofile.txt', 'Dofile', 'DOFILE', 'Makefile', 'MAKEFILE', 'makefile', 'mkfile']
	else:
		default_files = [filename]
	for file_name in default_files:
		fi = None
		try:
			fi = open(file_name, 'r')
			fi.close()
			return file_name
		except IOError:
			continue
	return None


def parse_file(filename):
	fi = open(filename, 'r')
	sess = _mk_session()
	for line in fi:
		parse_line(sess, line)
	fi.close()
	return sess.sections, sess.data


def parse_line(sess, line):
	if string.strip(line) == '':
		return
	tokens = string.split(line)
	if len(tokens) == 0:
		return
	else:
		if tokens[0] == '':
			return
		elif tokens[0][0] == '#':
			_parse_for_section(sess, line)
		elif tokens[0][-1] == ':' or (len(tokens) > 1 and tokens[1][0] == ':'):
			_parse_for_project(sess, line)
		else:
			_parse_for_file(sess, line)


def remove_symbols(line, symbols):
	if len(symbols) == 0:
		return [line]
	sym = symbols[0]
	if sym == ' ':
		tokens = string.split(line)
	else:
		tokens = string.split(line, sym)
	new_tokens = []
	for i in range(len(tokens)):
		if tokens[i] != '':
			new_tokens += [tokens[i]]
	tokens = []
	for token in new_tokens:
		tokens += remove_symbols(token, symbols[1:])
	return tokens


def _parse_for_section(sess, line):
	tokens = remove_symbols(line, [' ','#','='])
	cmd = string.lower(tokens[0])
	if sess.do_declaired == True:
		if len(tokens) == 2:
			_one_arg_commands[cmd](sess, tokens[1])
		elif len(tokens) == 1:
			_no_arg_commands[cmd](sess)
	else:
		if len(tokens) == 1:
			_no_arg_commands[cmd](sess)
		

def _parse_for_project(sess, line):
	if sess.do_declaired == False or sess.current_section == None:
		return
	tokens = remove_symbols(line, [' ',':'])
	if len(tokens) == 2 and tokens[1] == '':
		tokens = tokens[:1]
	if len(tokens) == 1:
		tokens[0] = string.strip(tokens[0])
		if sess.current_section != None:
			if string.lower(tokens[0]) == "register":
				_mk_project(tokens[0], sess.current_section)
				sess.current_project = None
			else:	
				sess.current_project = _mk_project(tokens[0], sess.current_section)


def _parse_for_file(sess, line):
	if sess.do_declaired == False:
		return
	tokens = string.split(line)
	if sess.current_project != None:
		for word in tokens:
			if word != '':
				sess.current_project.files += [word]


