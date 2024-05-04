import time


def better_print(text: str, delay: float = .01, newLine: bool = True):
    r"""Prints text

    Prints the given text letter by letter to the command line using the specified delay

    Parameters
    ----------
    text: str
        The text that is printed letter by letter

    delay: Optional[float]
        Changes the time between each printed letter
        DEFAULT: .01
    
    newLine: Optional[bool]
        whether to add a new line at the end or not
        DEFAULT: True
    """
    
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    if newLine:
        print('')