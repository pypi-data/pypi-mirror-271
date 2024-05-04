from os import system
from string import digits
import random
from pygetwindow import getActiveWindowTitle
from pynput.keyboard import Listener, Key, KeyCode
from .color import foreground, background

def clear() -> None:
	system("cls")

class ChoiceInterface:
	type __key = Key | KeyCode

	def __init__(
		self, *,
		textColor: foreground = foreground.WHITE,
		highlightTextColor: foreground = foreground.BLACK,
		highlightColor: background = background.WHITE,
		confirmKey: list[__key] | tuple[__key, ...] | __key = (Key.enter, Key.right),
		cancelKey: list[__key] | tuple[__key, ...] | __key = Key.esc,
		choicesSurround: str = "",
		addArrowToSelected: bool = False
	) -> None:
		r"""
		Creates the callable ChoiceInterface instance
		:param textColor:
		:param highlightTextColor:
		:param highlightColor:
		:param confirmKey:
		:param cancelKey:
		:param choicesSurround:
		:param addArrowToSelected:
		"""
		cfKey = confirmKey if isinstance(confirmKey, list) else [confirmKey]
		ccKey = cancelKey if isinstance(cancelKey, list) else [cancelKey]
		if set(cfKey) & set(ccKey):
			raise ValueError("values in confirmKey and cancelKey may not overlap!")
		self.confirmKeys = cfKey
		self.cancelKeys = ccKey
		self.textColor = textColor
		self.hlTextColor = highlightTextColor
		self.hlColor = highlightColor
		self.choicesSurround = choicesSurround
		self.addArrowToSelected = addArrowToSelected
		self.terminalWindowTitle = "Choice Interface {" + "".join(random.choices(digits, k=10)) + "}"
		self.lastKeyPressed = None

	def __call__(
			self,
			choices: list[str],
			prefix: str = "",
			suffix: str = "",
			selected: int = 0,
			minimumHighlightLength: int = -1,
			terminalTitleBefore: str = "Terminal"
		) -> int:
		r"""
		Starts the interface
		:param choices:
		:param prefix:
		:param suffix:
		:param selected:
		:param minimumHighlightLength:
		:param terminalTitleBefore:
		:return:
		"""
		system(f"TITLE {self.terminalWindowTitle}")

		if len(choices) <= 1 or (not (isinstance(choices, list) and all([isinstance(x, str) for x in choices]))):
			raise ValueError("Parameter 'lines' must be of length >= 2 and of type list[str]")
		if 0 > selected >= len(choices):
			raise ValueError(
				"Parameter 'selected' must be index of line in 'lines' and may therefore not be bigger than the "
				"biggest index of 'lines' or smaller than 0"
			)

		hlLen = minimumHighlightLength if (minimumHighlightLength >= 0 and
		                                   not (any([self.choicesSurround, self.addArrowToSelected]))) \
										else max([len(line) for line in choices]) + abs(minimumHighlightLength)

		while True:
			clear()
			if prefix:
				print(self.textColor.value + prefix+foreground.RESET.value)

			for i, line in enumerate(choices):
				_out = ''
				if i == selected:
					if not any([self.choicesSurround, self.addArrowToSelected]):
						_out = f"{self.hlColor.value+self.hlTextColor.value}{line:<{hlLen}}{foreground.RESET.value}"
					elif self.addArrowToSelected:
						_out = f"{self.hlColor.value+self.hlTextColor.value}{line+" >":<{hlLen+2}}{foreground.RESET.value}"
				else:
					_out = self.textColor.value+line+foreground.RESET.value
				if self.choicesSurround:
					_out = self.choicesSurround+_out+self.choicesSurround
				print(_out)

			if suffix:
				print(self.textColor.value+prefix+foreground.RESET.value)

			key = self._waitForKey()

			if key == Key.down and selected != len(choices)-1:
				selected += 1
			elif key == Key.up and selected != 0:
				selected -= 1
			elif key in self.confirmKeys:
				if key == Key.enter: input()
				system(f"TITLE {terminalTitleBefore}")
				return selected
			elif key in self.cancelKeys:
				if key == Key.enter: input()
				system(f"TITLE {terminalTitleBefore}")
				return -1
			elif key in [Key.down, Key.up]:
				pass
			else:
				raise Exception("Somehow, Somewhere, Something went wrong :/")

	def _waitForKey(self) -> __key | None:
		lst = Listener(on_press=lambda key: self._onKeyPress(key, lst))
		lst.start()
		lst.join()
		return self.__lastKeyPressed

	def _onKeyPress(self, key: __key | None, lst: Listener) -> None:
		if getActiveWindowTitle() != self.terminalWindowTitle:
			return
		self.__lastKeyPressed = key
		if self.__lastKeyPressed in self.confirmKeys+self.cancelKeys+[Key.up, Key.down]:
			lst.stop()