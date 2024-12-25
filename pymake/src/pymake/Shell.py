import subprocess
import re

class Shell:
	def run_cmd(self, cmd):
		# 安全的方式执行命令
		if not self.__comment__(cmd):
			result = subprocess.run(cmd, stdout=subprocess.PIPE)
			print(result.stdout.decode("utf-8"))
	
	def __comment__(cls, string) -> bool:
		pattern = r'^#.*'
		if re.match(pattern, string):
			return True
		else:
			return False
