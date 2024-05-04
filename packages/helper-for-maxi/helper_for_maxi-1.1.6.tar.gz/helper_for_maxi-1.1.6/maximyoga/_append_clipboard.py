import pyperclip

def append_clipboard(text: str) -> str:
    r"""
    Appends the given text to the clipboard
    :param text:
    :return: str
    """
    pyperclip.copy(text)
    return text