#! /usr/bin/python3
# Author: Ulas Askan
# Date: 5 Oct 2016
# Python version: 3.4 
# This program takes a path where all the files in the input directory and all the sub-directories in a Linux filesystem 
# and searches for a user input string. The search is case sensitive and the grep -i has not been implemented
# The search simulates Regular expressions. The program can search for text anywhere in the opened file using the (a) option,
# the beginning of each line (^) or the end of lines ($)
# The program checks if the files in subdirectories are readable. If not readable the program does not attempt to search these.
# The program checks if the files in subdirectories are binary or text. When binary files are encountered the program does not 
# attempt to search these either.

import os
import re

### Function for checking if the files have read permission
def AccessOK(pathin):
	PermDenied = []
	PathOK = []
	if not os.access(pathin, os.R_OK):
		PermDenied.append(pathin)		
	for path, dirs, files in os.walk(pathin):
		for dir in dirs:
			dir = os.path.join(path, dir)
			if not os.access(dir, os.R_OK):
				PermDenied.append(dir)
		for file in files:
			file = os.path.join(path, file)
			if not os.access(file, os.R_OK):
				PermDenied.append(file)
			else:
				PathOK.append(file)
	return (PathOK, PermDenied)

### Function for determining if the files are text or binary files
def TextOrBinary (FilePath):
	tFiles = []
	bFiles = []
	for CurrentFile in FilePath:
		try:
			with open(CurrentFile, "r") as tx:
				for line in iter(tx.readline, ''):
					pass
				tFiles.append(CurrentFile)
		except UnicodeDecodeError:
			pass  
			bFiles.append(CurrentFile)
		except IsADirectoryError:
			pass
	return(tFiles, bFiles)

### Function for searching for string anywhere in the files searched
def anywhere(pathlist, Term):
	for CurrentFile in pathlist:
		if os.access(CurrentFile, os.R_OK):
			with open(CurrentFile, 'rt') as openFile:
				for line in openFile:
					if Term in line:
						print (CurrentFile, ":", line.strip("\n\r"))
		if not os.access(CurrentFile, os.R_OK):
			break

### Function for searching for string at the beginning of the lines in the files searched
def beginning (pathlist, Term):
	for CurrentFile in pathlist:
		if os.access(CurrentFile, os.R_OK):
			with open(CurrentFile, 'rt') as openFile:
				for line in openFile:
					CurrentLine = line
					regex = re.match(Term, CurrentLine)
					if regex:
						print (CurrentFile, ':', line.strip("\n\r"))
		if not os.access(CurrentFile, os.R_OK):
			break

### Function for searching for string at the end of the lines in the files searched
def end(pathlist, Term):
	for CurrentFile in pathlist:
		if os.access(CurrentFile, os.R_OK):
			with open(CurrentFile, 'rt') as openFile:
				for line in openFile:
					CurrentLine = line
					if re.search(Term+r'$', CurrentLine):
						print (CurrentFile, ':', line.strip("\n\r"))
		if not os.access(CurrentFile, os.R_OK):
			break

def Main():
	Location = input('Type in the file/folder to search:  ')
	while os.path.exists(Location) is False:
		print ("Invalid file/folder name, please try again!")
		Location = input('Type in the file/folder to search:  ')

	Search = input('Type string to search:  ')
	print ("Choose an option: \n \ta - Search anywhere in the line \n \t^ - Search beginning of a line \n\t$ - Search end of a line ")
	option = input('a/^/$:  ')
	while option not in ('a', '^', '$'):
		print ("Invalid option!")
		option = input('a/^/$:  ')

	PathOK, PermDenied = AccessOK(Location)
	tFiles, bFiles = TextOrBinary(PathOK)	
	
	if option == "a":
		anywhere(tFiles, Search)
		for i in bFiles:
			print("Binary File:\t", i)
		for j in PermDenied:
			print(j, ": Permission denied")

	elif option == "^":
		beginning(tFiles, Search)
		for i in bFiles:
			print("Binary File:\t", i)
		for j in PermDenied:
			print(j, ": Permission denied")

	elif option == "$":
		end(tFiles, Search)
		for i in bFiles:
			print("Binary File:\t", i)
		for j in PermDenied:
			print(j, ": Permission denied")

if __name__ == "__main__":
	Main()
	print("\n")

