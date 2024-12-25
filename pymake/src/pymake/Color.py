# https://github.com/pypa/pipx/blob/main/src/pipx/colors.py

class Color:
	def __init__(self):
		self.style = {
	    "header": "\033[95m",
	    "blue":"\033[94m",
	    "green":"\033[92m",
	    "yellow":"\033[93m",
	    "red": "\033[91m",
	    "orange": "\033[93m",
	    "purple": "\033[95m",
	    "bold" : "\033[1m",
	    "cyan": "\033[96m",
	    "underline": "\033[4m",
	    "end": "\033[0m"
	    }
	def stylize_text(self, style: str, x: str) -> str:
		text_style = self.style.get(style)
		return f"{text_style}{x}{self.style['end']}"
