from typing import Optional
from .better_input import better_input as BetterInput
from .terminal import Terminal


def better_color_input(text: str = None, beforeColor: Optional[Terminal.color.foreground] = Terminal.color.RESET, delay: float = .01):
    r"""Gets an input

    Prints the given text letter by letter using the specified delay and gets an input() after

    Parameters
    ----------
    text: Optional[str]
        The text that is printed letter by letter
        DEFAULT: None
    
    beforeColor: Optional[Terminal.color.foreground]
        The color to change back to after getting the input
        DEFAULT: Terminal.color.RESET

    delay: Optional[float]
        Changes the time between each printed letter
        DEFAULT: .01
    """
    if text is not None:
        res = BetterInput(text, Terminal.color.foreground.FCYAN, delay)
    else:
        res = BetterInput(end=Terminal.color.foreground.FCYAN, delay=delay)
    if beforeColor is not None:
        print(beforeColor, end="")
    return res