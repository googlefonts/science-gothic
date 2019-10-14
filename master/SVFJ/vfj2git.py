# encoding:	utf-8
# ----------------------------------------------------
# SCRIPT: 	vfj2git
# DESC:		A tool for manipulating VFJ fonts into Git friendly format
# ----------------------------------------------------
# (C) Vassil Kateliev, 2019  (http://www.kateliev.com)
# (C) Karandash Type Foundry (http://www.karandash.eu)
# ----------------------------------------------------

# No warranties. By using this you agree
# that you use it at your own risk!

from __future__ import absolute_import, print_function, unicode_literals
import os, sys
import vfjLib

__version__ = '0.0.2'

# - String --------------------------------
help_str='''VFJ2GIT: A tool for manipulating VFJ fonts into Git friendly format
Usage:
	vfj2git --merge <pathname (SVFJ)> : Merge a split SVFJ format
	vfj2git --split <filename (VFJ)> : Split VFJ font file
'''
# - Init ----------------------------------
basePath = os.getcwd()
run_args = sys.argv[1:]

# - RUN ----------------------------------
if '--merge' in run_args:
	file_name = run_args[run_args.index('--merge') + 1]
	new_font = vfjLib.vfjFont()
	new_font.open(file_name, merge=True)
	new_font.save('%s.%s' %(file_name.split('.')[0],'vfj'))
	print('\nVFJ2GIT:\tDone merging %s.' %file_name)

if '--split' in run_args:
	file_name = run_args[run_args.index('--split') + 1]
	new_font = vfjLib.vfjFont(file_name)
	new_font.save(split=True)
	print('\nVFJ2GIT:\tDone splitting %s.' %file_name)

if '--help' in run_args:
	print(help_str)
	print(__version__)
	
