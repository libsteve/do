# do

A Client-side Wrapper for the RIT Computer Science Department's try program.

## Why?

try is a program installed on all RIT CS lab machines. It is a utilty for submitting, compiling, and testing students' projects.

The usability of try is minimal. Newcomers to the CS department have a hard time understanding how to use it, and students who prefer to work on their own computers are required to first transfer all of their work over to a RIT CS lab machine before they can submit their finished work.

The process of moveing all files over to the RIT CS machine can become tedious, cumbersome, and invasive to a productive workflow.

On top of that, there is no automation associated with try. The command must be run manually, and the class, project-name, and long list of files associated with the project must be manually entered with the arguments of the program.

Over all, although try is a useful utility for the submission of students' projects in theory, the lack of automation proves the utility to be ineffictive.

## How will do solve this problem?

do will allow students to automate the process of transferring their project files form their computers to the RIT CS lab machines and running try with all the appropriate files for the proper class and project.

do will read a file containing information about the class, project, and associated files that can be placed directly into any Makefile. do will then copy the files onto an RIT CS machine and run try for the student, providing the student with try's output.

## dofile Syntax

The dofile syntax can be placed within a 'dofile' or directly within a Makefile. do will look for a 'dofile', but if none is found, do will use any Makefile found.

Declare all lines following as dofile syntax:

	'#' 'dofile'

Declaring the class:

	'#' 'class' ['='] <class_name>
	
Declaring the project:

	<project_name> ':'
	
Declaring files:

	<file_name>*
	
Declare the end of the dofile segment:

	'#' 'enddo'
	
dofile example:

	#dofile

	#class = vcss243
	
	register:
	
	lab01:
		file1 file2 file3
		
	lab02:
		fileA
		fileB
		
	#class cs4
	
	register:
	
	project1:
		README
		file1.cpp file1.h
		file2.cpp file2.h

This dofile descripes the class `vcss243`, which has:

* a `lab01` project with files `file1`, `file2`, and `file3`
* a `register` project

This dotfile also describes the class `cs4`, which has:

* a `register` project
* a `project1` project with files `REAMDE`, `file1.cpp`, `file1.h`, `file2.cpp`, and `file2.h`

Notice that the projects named `register` don't have files associated with them. `register` is a special project that will register the user with the try program. do will automatically submit the required `/dev/null` file with the `register` project. If a `register` project has any files associated with it, do will ignore them.

Notice that there is no `#enddo` in the example. `#enddo` is only needed to let do ignore a section of the file.

## Resources

do uses paramiko 1.7.7.1 for ssh and sftp within python. http://www.lag.net/paramiko/