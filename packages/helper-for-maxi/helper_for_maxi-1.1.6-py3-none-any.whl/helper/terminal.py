import random


class Terminal:
    r"""Functions & Stuff for the Windows Terminal

    Contains classes and Functions to use for/in the Windows Terminal

    Subclasses
    ----------
    color:
        returns escape sequences to manipulate the color of the Terminal when printed
    """

    class color:
        r"""Manipulates the color of the Terminal

        Uses special character sequences to manipulate the color of the Terminal when printed out

        Options
        -------
        RESET:
            When printed out: Restores the colors of the Terminal to the Default
        
        Subclasses
        ----------
        foreground:
            Manipulates the foreground/text color.
            Also contains Bold and Underline options for the Font

        background:
            Manipulates the background color
        """

        RESET = '\033[0m'

        class foreground:
            DEFAULT = '\033[0m'
            BOLD = '\033[1m'
            noBOLD = '\033[22m'
            UNDERLINE = '\033[4m'
            noUNDERLINE = '\033[24m'
            SWAPCOLOR = '\033[7m'
            noSWAPCOLOR = '\033[27m'
            FBLACK = '\033[30m'
            FRED = '\033[31m'
            FGREEN = '\033[32m'
            FYELLOW = '\033[33m'
            FBLUE = '\033[34m'
            FMAGENTA = '\033[35m'
            FCYAN = '\033[36m'
            FWHITE = '\033[37m'
            FDEFAULT = '\033[39m'
            FLBLACK = '\033[90m'
            FLRED = '\033[91m'
            FLGREEN = '\033[92m'
            FLYELLOW = '\033[93m'
            FLBLUE = '\033[94m'
            FLMAGENTA = '\033[95m'
            FLCYAN = '\033[96m'
            FLWHITE = '\033[97m'

            colorList = [DEFAULT, FRED, FGREEN, FYELLOW, FBLUE, FMAGENTA, FCYAN, FWHITE, FDEFAULT, 
                         FLBLACK, FLRED, FLGREEN, FLYELLOW, FLBLUE, FLMAGENTA, FLCYAN, FLWHITE]
            def random():
                colorList = Terminal.color.foreground.colorList
                return random.choice(colorList)

        class background:
            DEFAULT = '\033[0m'
            SWAPCOLOR = '\033[7m'
            noSWAPCOLOR = '\033[27m'
            BBLACK = '\033[40m'
            BRED = '\033[41m'
            BGREEN = '\033[42m'
            BYELLOW = '\033[43m'
            BBLUE = '\033[44m'
            BMAGENTA = '\033[45m'
            BCYAN = '\033[46m'
            BWHITE = '\033[47m'
            BDEFAULT = '\033[49m'
            BLBLACK = '\033[100m'
            BLRED = '\033[101m'
            BLGREEN = '\033[102m'
            BLYELLOW = '\033[103m'
            BLBLUE = '\033[104m'
            BLMAGENTA = '\033[105m'
            BLCYAN = '\033[106m'
            BLWHITE = '\033[107m'

            colorList = [DEFAULT, BBLACK, BRED, BGREEN, BYELLOW, BBLUE, BMAGENTA, BCYAN, BWHITE,
                         BDEFAULT, BLBLACK, BLRED, BLGREEN, BLYELLOW, BLBLUE, BLMAGENTA, BLCYAN, BLWHITE]
            def random():
                colorList = Terminal.color.background.colorList
                return random.choice(colorList)