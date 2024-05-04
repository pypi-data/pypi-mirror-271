from .better_print import better_print as BetterPrint


def better_input(text: str = "", delay: float = .01):
    r"""Gets an input

    Prints the given text letter by letter using the specified delay and gets an input() after

    Parameters
    ----------
    text: Optional[str]
        The text that is printed letter by letter
        DEFAULT: ""

    delay: Optional[float]
        Changes the time between each printed letter
        DEFAULT: .01
    """
    
    if text:
        BetterPrint(text, delay, False)
    res = input()
    return res