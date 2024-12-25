from pymake.MakeMap import MakeMap
from pymake.Shell import Shell
from pymake.Color import Color
from pymake import __version__
from pathlib import Path
from itertools import chain
import sys

class Make:
	def __init__(self):
		self.color = Color().stylize_text
		self.makefile = ['makefile', 'Makefile']

		self.stack_list = []
		self.key_val = {}
		self.defaultList = ['.PHONY', 'default']
		
		if self.makefile:
			mk = self.check_makefile()
			self.make_map = MakeMap(mk)
			self.data = self.make_map.data
		
	
	def init(self, key='default'):
		
		while key:
			key_val = self.data['recipes'].get(key)
			if key_val:
				self.stack_list.append({
					'key': key,
					'cmd':key_val.get('cmd')
					})
				key = key_val.get('src')
			else:
				print(f"{self.color('cyan','no found key.')}")
				sys.exit(1)
				break
		
		while len(self.stack_list):
			stacks = self.stack_list.pop()
			print(f"[{self.color('green', stacks.get('key'))}]")
			for cmd in stacks.get('cmd'):
				Shell().run_cmd(cmd)
				
	def __flattern_cmd(self):
		for (k,v) in self.data['magic'].items():
			cmds_list = v['cmd']
			v['cmd'] = list(chain.from_iterable(cmds_list))
			self.data['magic'][k] = v
	
	def run_magic(self):
		self.__flattern_cmd()
		print(f"[{self.color('orange','magic')}]")
		for (k, v) in self.data['magic'].items():
			for cmd in v['cmd']:
				Shell().run_cmd(cmd)
		
	def check_makefile(self):
		mk = ''
		error_msg = 'Error: not found makefile or Makefile'
		for filename in self.makefile:
			if Path(filename).exists():
				mk = filename
				break
		if not mk:
			print(self.color('red', error_msg))
			sys.exit(1)
		return mk
	
	@staticmethod
	def get_version():
		return __version__
	
	def runner(self, arg):
		if arg == '--list':
			print(f"pymake {self.get_version()}\n")
			for (k, v) in self.data['recipes'].items():
				if k not in self.defaultList:
					print(f"{self.color('green',k)}: {v['comment']}")

