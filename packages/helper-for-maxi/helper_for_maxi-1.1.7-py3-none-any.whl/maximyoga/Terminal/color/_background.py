from enum import Enum

class background(Enum):
	SWAPCOLOR = '\033[7m'
	BLACK = '\033[40m'
	RED = '\033[41m'
	GREEN = '\033[42m'
	YELLOW = '\033[43m'
	BLUE = '\033[44m'
	MAGENTA = '\033[45m'
	CYAN = '\033[46m'
	WHITE = '\033[47m'
	DEFAULT = '\033[49m'
	LBLACK = '\033[100m'
	LRED = '\033[101m'
	LGREEN = '\033[102m'
	LYELLOW = '\033[103m'
	LBLUE = '\033[104m'
	LMAGENTA = '\033[105m'
	LCYAN = '\033[106m'
	LWHITE = '\033[107m'

	RESET = '\033[0m'
