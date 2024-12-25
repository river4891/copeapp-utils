#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import subprocess
import re

__version__ = "0.0.0.1"

class Shell:
	def __run_cmd(cls, cmd):
	# 安全的方式执行命令
		result = subprocess.run(cmd, stdout=subprocess.PIPE)
		print(result.stdout.decode("utf-8"))
	
	def __comment__(cls, string) -> bool:
		pattern = r'^#.*'
		if re.match(pattern, string):
			return True
		else:
			return False
	
	def get(self, file):
		line = file.readline()
		while line:
			if not self.__comment__(line):
				cmd = line.strip().split(" ")
				self.__run_cmd(cmd)
			line = file.readline()
            
def main():
    parser = argparse.ArgumentParser(description="Read the content of a file.")
    parser.add_argument("file", type=argparse.FileType('r'), help="Name of the file to read")
    args = parser.parse_args()
    Shell().get(args.file)

if __name__ == "__main__":
    main()