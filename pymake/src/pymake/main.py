#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pymake.Make import Make
import sys
import argparse

def cli():
	make = Make()
	parser = argparse.ArgumentParser(description="construct tool for codeapp like make.")
	parser.add_argument('recipes',nargs='?', help="receive a recipe value")
	parser.add_argument('--list', '-l', action='store_true', help="list recipes in makefile.")
	parser.add_argument('--version', '-V', action='version', version=make.get_version(), help='show version information')

	args = parser.parse_args()
	
	if args.list:
		make.runner('--list')
		
	if args.recipes:
		make.run_magic()
		make.init(args.recipes)
			

def main():
	cli()
	
if __name__ == '__main__':
	main()
