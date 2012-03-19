from reader import *

def get_session():
	x = session()
	x.current_section = None
	x.current_project = None
	x.sections = []
	x.do_declaired = False
	return x

_success = 0
_successes = []
_failure = 0
_failures = []

def test(line, expected, s=None, name=""):
	if s == None:
		s = get_session()
	parse_line(s, line)
	test_proper(s, expected, name)

def test_s(s, line, expected, name=""):
	test(line, expected, s=s, name=name)

def test_proper(s, expected, name=""):
	if expected(s):
		global _success
		_success += 1
		global _successes
		_successes += [name]
	else:
		global _failures
		_failures += [name]
		global _failure
		_failure += 1

#####
## testing begin
#####

#####
## test find file

test_proper(find_file(""), lambda s: s == "dofile", name="find file no file given")

test_proper(find_file("dofile"), lambda s: s == "dofile", name="find file dofile")

test_proper(find_file("bad_file"), lambda s: s == None, name="find file bad file")

test_proper(find_file("reader.py"), lambda s: s == "reader.py", name="good file")





#####
## test dofile decleration

test("", lambda s: s.do_declaired == False, name="no dofile")

test("#dofile", lambda s: s.do_declaired == True, name="dofile declaired")

sess = get_session()
parse_line(sess, "#dofile")
test_s(sess, "#enddo", lambda s: s.do_declaired == False, name="enddo declaired")





#####
## test class generation

#without dofile decleration

test("#class=vcss243", lambda s: s.current_section == None, name="class with equals no dofile")

test("#class cs4", lambda s: s.current_section == None, name="class no equals no dofile")

#with dofile decleration
sess = get_session()
parse_line(sess, "#dofile")

test_s(sess, "#class=vcss243", lambda s: s.current_section.name == "vcss243", name="class with equals")

test_s(sess, "#class cs4", lambda s: s.current_section.name == "cs4", name="class no equals")






#####
## test project generation

test("lab01:", lambda s: s.current_project == None, name="lab no class")

test("register:", lambda s: s.current_project == None, name="register no class")

#create class for project testing
sess = get_session()
parse_line(sess, "#dofile")
parse_line(sess, "#class=vcss243")

test_s(sess, "register:", lambda s: s.current_project == None, name="register with class")
test_proper(sess, lambda s: len(s.current_section.projects) == 1 and s.current_section.projects[0].name == "register", name="register with class success")

test_s(sess, "lab01:", lambda s: s.current_project != None and s.current_project.name == "lab01", name="lab with class")
test_proper(sess, lambda s: len(s.current_section.projects) == 2 and s.current_section.projects[1].name == "lab01", name="lab with class success")






#####
## test file adding

#create class for project testing
sess = get_session()
parse_line(sess, "#dofile")
parse_line(sess, "#class=vcss243")
parse_line(sess, "lab01:")

test_s(sess, "file1 file2", lambda s: len(s.current_project.files) == 2 and s.current_project.files[0] == "file1" and s.current_project.files[1] == "file2", name="file on lab")




######
## testing end
######

if _failure == 0:
	print("Success!\n")
else:
	print(str(_success) + " Successes\n")
	print(_successes)
	print("\n")
	print(str(_failure) + " Failures\n")
	print(_failures)




