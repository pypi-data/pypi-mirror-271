from ._better_print import better_print as BetterPrint


def better_input(*args, sep: str = ' ', delay: float = .01) -> str:
	r"""
	Prints args seperated by sep with the given delay between each character and gets an input
	:param args:
	:param sep:
	:param delay:
	:return: str
	"""

	if not args:
		text = ''
	else:
		text = sep.join(args)

	if text:
		BetterPrint(text, delay=delay, end='')
	res = input()
	return res
