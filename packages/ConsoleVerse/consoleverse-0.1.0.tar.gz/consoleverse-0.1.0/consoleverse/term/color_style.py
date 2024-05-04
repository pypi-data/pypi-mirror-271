"""
This module contains the classes for coloring the text and background of the text.

Classes:
- ColorText: Used to color the text.
- ColorBackground: Used to color the background of the text.
- StyleText: Used to style the text.

Example usage:
    >>> from consoleverse.term.colors import ColorText, ColorBackground, StyleText
    >>> text = ColorText()
    >>> bg = ColorBackground()
    >>> style = StyleText()
    >>> print(text['RED'] + bg['BG_WHITE'] + style['BOLD'] + 'Hello ConsoleVerse!' + text.reset())

The above code will print 'Hello ConsoleVerse!' in bold red text with a white background.

The following are the available text colors:
    - BLACK
    - RED
    - GREEN
    - YELLOW
    - BLUE
    - MAGENTA
    - CYAN
    - WHITE

The following are the available background colors:
    - BG_BLACK
    - BG_RED
    - BG_GREEN
    - BG_YELLOW
    - BG_BLUE
    - BG_MAGENTA
    - BG_CYAN
    - BG_WHITE

The following are the available text styles:
    - BOLD
    - DIM
    - UNDERLINE
    - BLINK
    - REVERSE
    - HIDDEN
"""

from consoleverse.term.exceptions.ex_colors import (
    ColorTextError,
    ColorBackgroundError,
    ColorStyleError
)


class _ColorBase:
    """
    This class is used as a base class for the color classes.

    It contains the methods for starting and ending the color formatting.
    """
    RESET_FORMAT_COLOR: int = 0
    START_FORMAT_COLOR: str = '\033[{}m'
    END_FORMAT_COLOR: str   = START_FORMAT_COLOR.format(RESET_FORMAT_COLOR)

    def start(self, color):
        return self.START_FORMAT_COLOR.format(color)

    def end(self):
        return self.END_FORMAT_COLOR

    def reset(self):
        return self.END_FORMAT_COLOR


class ColorTextCode(_ColorBase):
    """
    This class is used to store the color codes for the text.
    """
    BLACK_CODE: int   = 30
    RED_CODE: int     = 31
    GREEN_CODE: int   = 32
    YELLOW_CODE: int  = 33
    BLUE_CODE: int    = 34
    MAGENTA_CODE: int = 35
    CYAN_CODE: int    = 36
    WHITE_CODE: int   = 37


class ColorText(ColorTextCode):
    """
    This class is used to color the text.

    Example usage:
        >>> from consoleverse.term.colors import ColorText
        >>> text = ColorText()
        >>> print(text['RED'] + 'Hello ConsoleVerse!' + text.reset())

    The above code will print 'Hello ConsoleVerse!' in red.

    The following are the available text colors:
        - BLACK
        - RED
        - GREEN
        - YELLOW
        - BLUE
        - MAGENTA
        - CYAN
        - WHITE
    """
    BLACK   = 'BLACK'
    RED     = 'RED'
    GREEN   = 'GREEN'
    YELLOW  = 'YELLOW'
    BLUE    = 'BLUE'
    MAGENTA = 'MAGENTA'
    CYAN    = 'CYAN'
    WHITE   = 'WHITE'

    def __init__(self):
        self.COLORS = {
            self.BLACK   : self.start(self.BLACK_CODE),
            self.RED     : self.start(self.RED_CODE),
            self.GREEN   : self.start(self.GREEN_CODE),
            self.YELLOW  : self.start(self.YELLOW_CODE),
            self.BLUE    : self.start(self.BLUE_CODE),
            self.MAGENTA : self.start(self.MAGENTA_CODE),
            self.CYAN    : self.start(self.CYAN_CODE),
            self.WHITE   : self.start(self.WHITE_CODE),
        }

        self.COLORS_LIST = list(self.COLORS.keys())

    def __getitem__(self, color):
        try:
            return self.COLORS[color.upper()]
        except KeyError:
            raise ColorTextError(color)

    def __contains__(self, color):
        if color:
            return color.upper() in self.COLORS

    def __str__(self):
        return str(self.COLORS_LIST)


class ColorBackgroundCode(_ColorBase):
    """
    This class is used to store the color codes for the background of the text.
    """
    BG_BLACK_CODE: int   = 40
    BG_RED_CODE: int     = 41
    BG_GREEN_CODE: int   = 42
    BG_YELLOW_CODE: int  = 43
    BG_BLUE_CODE: int    = 44
    BG_MAGENTA_CODE: int = 45
    BG_CYAN_CODE: int    = 46
    BG_WHITE_CODE: int   = 47


class ColorBackground(ColorBackgroundCode):
    """
    This class is used to color the background of a text.

    Example usage:
        >>> from consoleverse.term.colors import ColorBackground
        >>> bg = ColorBackground()
        >>> print(bg['BG_RED'] + 'Hello ConsoleVerse' + bg.reset())

    The above code will print 'Hello ConsoleVerse' with a red background.

    The following are the available background colors:
        - BG_BLACK
        - BG_RED
        - BG_GREEN
        - BG_YELLOW
        - BG_BLUE
        - BG_MAGENTA
        - BG_CYAN
        - BG_WHITE
    """
    BG_BLACK   = 'BG_BLACK'
    BG_RED     = 'BG_RED'
    BG_GREEN   = 'BG_GREEN'
    BG_YELLOW  = 'BG_YELLOW'
    BG_BLUE    = 'BG_BLUE'
    BG_MAGENTA = 'BG_MAGENTA'
    BG_CYAN    = 'BG_CYAN'
    BG_WHITE   = 'BG_WHITE'

    def __init__(self):
        self.BACKGROUNDS = {
            self.BG_BLACK   : self.start(self.BG_BLACK_CODE),
            self.BG_RED     : self.start(self.BG_RED_CODE),
            self.BG_GREEN   : self.start(self.BG_GREEN_CODE),
            self.BG_YELLOW  : self.start(self.BG_YELLOW_CODE),
            self.BG_BLUE    : self.start(self.BG_BLUE_CODE),
            self.BG_MAGENTA : self.start(self.BG_MAGENTA_CODE),
            self.BG_CYAN    : self.start(self.BG_CYAN_CODE),
            self.BG_WHITE   : self.start(self.BG_WHITE_CODE),
        }

        self.BACKGROUNDS_LIST = list(self.BACKGROUNDS.keys())

    def __getitem__(self, background):
        try:
            if 'BG_' not in background:
                background = f'BG_{background}'
            return self.BACKGROUNDS[background.upper()]
        except KeyError:
            raise ColorBackgroundError(background)

    def __contains__(self, background):
        if 'BG_' not in background:
                background = f'BG_{background}'
        return background.upper() in self.BACKGROUNDS

    def __str__(self):
        return str(self.BACKGROUNDS_LIST)


class StyleTextCode(_ColorBase):
    """
    This class is used to store the style codes for the text.
    """
    BOLD_CODE: int      = 1
    DIM_CODE: int       = 2
    UNDERLINE_CODE: int = 4
    BLINK_CODE: int     = 5
    REVERSE_CODE: int   = 7
    HIDDEN_CODE: int    = 8


class StyleText(StyleTextCode):
    """
    This class contains the styles for the text.

    Example usage:
        >>> from consoleverse.term.colors import StyleText
        >>> style = StyleText()
        >>> print(style['BOLD'] + 'Hello ConsoleVerse' + style.end())

    The above code will print 'Hello ConsoleVerse' in bold.

    The styles are:
        - BOLD
        - UNDERLINE
        - BLINK
        - REVERSE
        - HIDDEN
    """
    BOLD      = 'BOLD'
    DIM       = 'DIM'
    UNDERLINE = 'UNDERLINE'
    BLINK     = 'BLINK'
    REVERSE   = 'REVERSE'
    HIDDEN    = 'HIDDEN'

    def __init__(self):
        self.STYLES = {
            self.BOLD      : self.start(self.BOLD_CODE),
            self.DIM       : self.start(self.DIM_CODE),
            self.UNDERLINE : self.start(self.UNDERLINE_CODE),
            self.BLINK     : self.start(self.BLINK_CODE),
            self.REVERSE   : self.start(self.REVERSE_CODE),
            self.HIDDEN    : self.start(self.HIDDEN_CODE),
        }

        self.STYLES_LIST = list(self.STYLES.keys())

    def __getitem__(self, style):
        try:
            return self.STYLES[style.upper()]
        except KeyError:
            raise ColorStyleError(style)

    def __contains__(self, style):
        return style.upper() in self.STYLES

    def __str__(self):
        return str(self.STYLES_LIST)