import string


class section:
	pass


class project:
	pass


class session:
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


def _mk_session():
	x = session()
	x.current_section = None
	x.current_project = None
	x.sections = []
	x.do_declaired = False
	return x


def parse_file(filename):
	fi = open(filename, 'r')
	sess = _mk_session()
	for line in fi:
		parse_line(sess, line)
	fi.close()
	return sess.sections


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


def _parse_for_section(sess, line):
	# get rid of the first '#' and strip whitespace again
	good_line = string.strip(line)
	good_line = string.strip(good_line, '#')
	good_line = string.strip(good_line)
	tokens = string.split(good_line, '=')
	if len(tokens) == 1:
		tokens = string.split(good_line)
	if len(tokens) == 3 and tokens[2] == '':
		tokens = tokens[:2]
	if sess.do_declaired == True:
		if len(tokens) == 2:
			if string.lower(tokens[0]) == 'class':
				sess.current_section = _mk_section(tokens[1])
				sess.sections += [sess.current_section]
		elif len(tokens) == 1:
			if string.lower(toekns[0]) == 'enddo':
				sess.do_declaired = False
	else:
		if len(tokens) == 1:
			if string.lower(tokens[0]) == 'dofile':
				sess.do_declaired = True

		

def _parse_for_project(sess, line):
	if sess.do_declaired == False or sess.current_section == None:
		return
	good_line = string.strip(line)
	tokens = string.split(good_line, ':')
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


