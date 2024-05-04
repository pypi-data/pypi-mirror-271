import pyperclip

def append_clipboard(text: str) -> str:
    r"""copies text

    Copies / Appends the given text to the windows clipboard using the utf-8 encoding

    Parameters
    ----------
    text: str
        The text that is copied / appended to the clipboard
    """
    pyperclip.copy(text)
    return text