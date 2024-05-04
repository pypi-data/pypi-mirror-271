from .Terminal.color import foreground

def color_input(text: str = "", beforeColor: foreground = foreground.RESET):
    r"""
    Gets an input in CYAN. Resets the color to `beforeColor` afterwards
    :param text:
    :param beforeColor:
    :return:
    """
    if text:
        res = input(text + foreground.CYAN.value)
    else:
        res = input(foreground.CYAN.value)
    if beforeColor is not None:
        print(beforeColor.value, end="")
    return res