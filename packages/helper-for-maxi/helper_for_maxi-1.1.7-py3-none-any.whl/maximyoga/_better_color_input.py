from ._better_input import better_input as BetterInput
from .Terminal.color import foreground


def better_color_input(
		*args,
		sep: str = ' ',
		delay: float = .01,
		beforeColor: foreground = foreground.RESET
) -> str:
	r"""
	Prints args seperated by sep with the given delay between each character and gets an input in CYAN. Resets the
	color to `beforeColor` afterwards
	:param args:
	:param sep:
	:param delay:
	:param beforeColor:
	:return: str
	"""

	if not args:
		text = ""
	else:
		text = sep

	if text is not None:
		res = BetterInput(text, foreground.CYAN.value, delay=delay)
	else:
		res = BetterInput(foreground.CYAN.value, delay=delay)

	print(beforeColor.value, end="")

	return res