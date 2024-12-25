import re
from pymake.Color import Color
from pathlib import Path


class MakeMap:

	def __init__(self, makefile):
		self.recipes = Recipes()
		self.magic = Magic()
		self.color = Color().stylize_text
		self.choice = ''
		self.magic_data = {}
		self.data = {'recipes': {}, 'magic': {}}
		self.status = ''
		self.match = None
		self.makefile = makefile
		self.init()

	def init(self):
		try:
			with open(self.makefile, mode='r', encoding='utf-8') as file:
				for line in file:
					self.__set_choice(line)
					self.__set_status()
					

					if self.match and self.choice:
						
						self.data[self.choice][self.status] = {
						 'src': self.match.group('src'),
						 'comment': str(self.match.group('comment')).strip(),
						 'cmd': []
						}
					self.__token_cmd(line)
				#print(f"match:{self.match}, status:{self.status}")
		except FileNotFoundError:
			error_text = f'{self.makefile} not found.'
			raise Exception(self.color('red', error_text))

	def __set_status(self):
		new_targe = ''
		new_targe = (self.match and self.match.group('targe'))
		if new_targe:
			self.status = new_targe
			
	def __set_choice(self, text):
		new_choice = self.__test_match(text)
		if new_choice:
			self.choice = new_choice
			
	def __token_cmd(self, line: str):
		cmd = ''
		if re.match(r'^\t.*', line):
			cmd = line.strip()
			
		#print(cmd)
		
		if self.choice == 'magic' and cmd:
			cmd = self.magic.expand_cmd(cmd, self.magic_data['targe'], self.magic_data['src'])
			
			
		if self.status and cmd and self.choice:
			self.data[self.choice][self.status]['cmd'].append(cmd)
		

	
	def __test_match(self, text: str):
		if self.magic.test_match(text):
			self.match = self.magic.test_match(text)
			self.magic_data = self.magic.get_recipes(self.match)
			return 'magic'
		elif self.recipes.test_match(text):
			self.match = self.recipes.test_match(text)
			return 'recipes'
		else:
			self.match = ''
			return None

class Recipes:
	def test_match(cls, text: str):
		pattern = r'^(?P<targe>(?:(?:\w+/)+)?.[\w]+)(?:\s+)?:(?:\s+)?(?P<src>(?:(?:\w+/)+)?[.\w]+)?(?:\s+)?(?:#\s+?(?P<comment>.*))?'
		return re.match(pattern, text)
	
class Magic:
	def __init__(self):
		pass
		
	def get_recipes(cls, match):
		data = {
			'targe': match.group('targe'),
			'src': match.group('src'),
			'comment': match.group('comment')
		}
		return data
	
	def test_match(cls, text: str):
		pattern = r'^(?P<targe>(?:(?:\w+/)+)?%.[\w]+)(?:\s+)?:(?:\s+)?(?P<src>(?:(?:\w+/)+)?%[.\w]+)?(?:\s+)?(?:#\s+?(?P<comment>.*))?'
		return re.match(pattern, text)
		
	def parse_cmd(cls, text: str, targe: str, src: str):
		new_text = ''
		targe_magic = '$@'
		src_magic = '$^'
		new_text = text.replace(targe_magic, targe)
		new_text = str(new_text).replace(src_magic, src) 
		
		return new_text
	
	def expand_cmd(self, text: str, targe, src):
		cmd_list = []
		data_list = self.parse_recipes(targe, src)
		targe_list = data_list['targe_path']
		src_list = data_list['src_path']
		for (t, s) in zip(targe_list, src_list):
			cmd_list.append(self.parse_cmd(text, str(t), str(s)))
		return cmd_list
		
	def parse_recipes(cls, targe: str, src: str):
		src_pattern = src.replace('%', '(.*)')
		src_glob = src.replace('%', '*')
		targe_pattern = targe.replace('%', '\\1')
	
		src_path = sorted(Path('.').glob(src_glob))
		
		targe_path = list(map(lambda x: re.sub(rf"{src_pattern}", rf"{targe_pattern}", str(x)), src_path))
		
		#print(src_path, targe_path)
		return  {
			'src_path': src_path,
			'targe_path': targe_path
		}
		#targe_path = Path('.').glob(targe_pattren)

