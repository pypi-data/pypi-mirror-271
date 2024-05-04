"""
This module provides a collection of functions for working with the console.

Functions:
- init(...): Initializes the console configuration.
- clear_screen(): Clears the console screen.
- add_lvl(): Adds a new level to the console.
- del_lvl(): Deletes the last added level from the console.
- println(...): Prints a message to the console.
- inputln(...): Prints a message to the console and returns the user input.
- start_block(...): Starts a new message block with a given color and background color.
- end_block(...): Ends the current message block and prints a message.
- warning(...): Prints a warning message to the console.
- error(...): Prints an error message to the console.
- new_line(): Prints a new line to the console.
- line(...): Prints a horizontal line to the console.
- print_emoji_list(): Prints a list of supported emojis to the console.
- print_color_list(): Prints a list of supported colors to the console.
- print_style_list(): Prints a list of supported text styles to the console.
- print_matrix(...): Prints a matrix to the console.
- textbox(...): Prints a textbox to the console.
- progress_bar(...): Prints a progress bar to the console.
- print_tree(...): Prints a tree to the console.
- bar_chart(...): Prints a bar chart to the console.
- print_title(...): Prints a title to the console.

Constants:
- NAME: The name of the module.

Decorators:
- block(...): Decorator to create a block of text.

Notes:
- The console is managed by the Console class.
- The console configuration is managed by the Config class.
- The console colors are managed by the ColorText and ColorBackground classes.
- The console text styles are managed by the StyleText class.
- The console emojis are managed by the Emoji class.
- The console exceptions are managed by the exceptions module.
"""


from typing import (
    Any,
    List,
    Union,
    Callable
)
import functools
import os
import builtins

from consoleverse.config import lang
from consoleverse import term
from consoleverse import exceptions as ex


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          constants                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
NAME : str = 'ConsoleVerse'

__START_LANGS = {
    lang.Language()['en'] : 'START',
    lang.Language()['es'] : 'INICIA',
}

__END_LANGS = {
    lang.Language()['en'] : 'END',
    lang.Language()['es'] : 'TERMINA',
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                         decorators                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def block(
        message_block: Union[str, dict],
        text_color: str = 'BLUE',
        bg_color: str = ''
    ) -> Callable[..., Any]:
    """
    Decorator to create a block of text.

    Parameters
    ----------
    message_block : Union[str, dict]
        if is a str, then is the title of the block, if is a dict, then is the
        title is taken according to the language selected in the config file,
        e.g. {'en': 'Title', 'es': 'Título'} the title is printed is Title if the
        language is `en`, and Título if the language is `es`.

    text_color : str, optional
        The color of the message, by default BLUE

    bg_color : str, optional
        The background color of the message, by default has no color
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            message = message_block
            if isinstance(message_block, dict):
                message = message_block[lang.lang()]

            start_block(message, color=text_color, bg_color=bg_color)
            new_line()
            value = func(*args, **kwargs)
            new_line()
            end_block(message, color=text_color, bg_color=bg_color)
            return value
        return wrapped
    return decorator


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ~~                          functions                         ~~ #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class _ConsoleConfig:
    _indentation_type  : str = ' '
    _indentation_lvl   : str = ''
    _indentantion_size : int = 2
    _is_init : bool = False
    _autoreset_colors: bool = True

    @staticmethod
    def init(
        clear: bool = True,
        indentation_type: str = ' ',
        indentation_size: int = 2,
        autoreset_colors: bool = True
     ):
        """
        Initialize the console, and resert the indentation level

        Parameters
        ----------
        clear : bool, optional
            True to clear the screen and False is not, by default True
        """
        _ConsoleConfig._indentation_lvl = ''
        _ConsoleConfig._indentantion_size = indentation_size
        _ConsoleConfig._indentation_type  = indentation_type
        _ConsoleConfig._autoreset_colors  = autoreset_colors

        if clear:
            clear_screen()
        _ConsoleConfig._is_init = True

    @staticmethod
    def reset_config() -> None:
        """
        Reset the configuration of the console
        """
        _ConsoleConfig._indentation_type  = ' '
        _ConsoleConfig._indentation_lvl   = ''
        _ConsoleConfig._indentantion_size = 2
        _ConsoleConfig._is_init = False
        _ConsoleConfig._autoreset_colors = True

    @staticmethod
    def _init():
        """
        If the console still doesn't start, then start the console without
        indentation.
        """
        if not _ConsoleConfig._is_init:
            _ConsoleConfig._is_init = True
            _ConsoleConfig._indentation_lvl = ''

    @staticmethod
    def indentation_lvl() -> str:
        """
        Return the current indentation level

        Returns
        -------
        str
            The current indentation level
        """
        return _ConsoleConfig._indentation_lvl

    @staticmethod
    def add_indentation_lvl() -> None:
        """
        Add one level (indentation)
        """
        _ConsoleConfig._indentation_lvl += (
            _ConsoleConfig._indentation_type * _ConsoleConfig._indentantion_size
        )

    @staticmethod
    def del_indentation_lvl() -> None:
        """
        Substract one level (indentation)
        """
        _ConsoleConfig._indentation_lvl = \
            _ConsoleConfig._indentation_lvl[:-_ConsoleConfig._indentantion_size]


def init(
        clear: bool = True,
        indentation_type: str = ' ',
        indentation_size: int = 2,
        autoreset_colors: bool = True
    ) -> None:
    """
    Initialize the console, and resert the indentation level

    Parameters
    ----------
    clear : bool, optional
        True to clear the screen and False is not, by default True
    """
    _ConsoleConfig.init(
        clear=clear,
        indentation_type=indentation_type,
        indentation_size=indentation_size,
        autoreset_colors=autoreset_colors
    )


def reset_colors() -> None:
    """
    Reset the colors of the console
    """
    println(term.ColorText().reset(), end='')


def reset_config() -> None:
    """
    Reset the configuration of the console
    """
    _ConsoleConfig.reset_config()


def clear_screen():
    """
    Clear the console screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def add_lvl():
    """
    Add one level (indentation)
    """
    _ConsoleConfig.add_indentation_lvl()


def del_lvl():
    """
    Substract one level (indentation)
    """
    _ConsoleConfig.del_indentation_lvl()


def _colorize(
        text: str,
        color: str | None,
        bg_color: str | None,
        style: str | None,
        reset_console_colors: bool,
    ) -> str:
    """
    Colorize the text

    Parameters
    ----------
    text : str
        The text to colorize

    color : str
        The color of the text, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    bg_color : str
        The background color of the text, the color must be one of the `console.ColorBackground()`
        or `console.ColorText()` for all colors available; by default has no color

    style : str
        The style of the text, the style must be one of the `console.StyleText()`,
        by default has no style

    reset_console_colors : bool
        True to reset all colors, False is not necessary, by default `True`

    Returns
    -------
    str
        The colorized text
    """
    if color is None:
        color = ''
    if bg_color is None:
        bg_color = ''
    if style is None:
        style = ''

    ctext = term.ColorText()
    if color not in ctext and color != '':
        raise ex.ErrorNotDefinedColor(color)
    ctext = ctext[color] if color != '' else ''

    cbaground = term.ColorBackground()
    if bg_color not in cbaground and bg_color != '':
        raise ex.ErrorNotDefinedColor(bg_color)
    cbaground = cbaground[bg_color] if bg_color != '' else ''

    stext = term.StyleText()
    if style not in stext and style != '':
        raise ex.ErrorNotDefinedStyle(style)
    stext = stext[style] if style != '' else ''

    colorized_text = f'{ctext}{cbaground}{stext}{text}'

    if reset_console_colors:
        colorized_text += term.ColorText().reset()

    return colorized_text


def println(
        *message: Any,
        end: str = '\n',
        withlvl: bool = True,
        color: str | None = '',
        bg_color: str | None = '',
        reset_all_colors: bool = True,
        style: str | None = '',
        sep: str = ' ',
        **kwargs
    ) -> None:
    """
    Print the message to the console, the `endl` is the same as `end` in print function
    and is necessary print the message with the current indentation level and the color
    indicate.

    Parameters
    ----------
    message : Any
        Message to print to console

    end : str, optional
        The end of line, by default `\\n`

    withlvl : bool, optional
        True if the message should be printed with the current indentation
        False is not necessary, by default `True`

    color : str, optional
        The color of the message, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    bg_color : str, optional
        The background color of the message, the color must be one of the `console.ColorBackground()`
        or `console.ColorText()` for all colors available; by default has no color

    reset_all_colors : bool, optional
        True to reset all colors, False is not necessary, by default `True`

    style : str, optional
        The style of the message, the style must be one of the `console.StyleText()`,
        by default has no style

    sep : str, optional
        The separator between the values, by default is a space

    kwargs : dict
        Additional parameters to print the function
    """
    _ConsoleConfig._init()
    message_str: str = __to_string(*message, sep=sep)

    if withlvl:
        message_str = _ConsoleConfig.indentation_lvl() + message_str

    colorized_text: str = _colorize(
        text=message_str,
        color=color,
        bg_color=bg_color,
        style=style,
        reset_console_colors=reset_all_colors
    )
    builtins.print(colorized_text, end=end, **kwargs)


def __to_string(*values: Any, sep: str = ' ') -> str:
    """
    Convert the values to a string

    Parameters
    ----------
    values : Any
        The values to convert to a string

    sep : str, optional
        The separator between the values, by default is a space

    Returns
    -------
    str
        The string of the values
    """
    return sep.join([str(m) for m in values])


def start_block(*message: Any, color: str = 'BLUE', bg_color: str = '') -> None:
    """
    Start a block of messages

    Parameters
    ----------
    message : Any
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE

    bg_color : str, optional
        The background color of the title block, by default has no color
    """
    message_str: str = __to_string(*message)
    println(
        f'{__START_LANGS[lang.lang()]} {message_str.upper()}',
        color=color,
        bg_color=bg_color
    )
    add_lvl()


def end_block(
        *message: Any,
        color: str = 'BLUE',
        bg_color: str = '',
        style: str = ''
    ) -> None:
    """
    End a block of messages

    Parameters
    ----------
    message : Any
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE

    bg_color : str, optional
        The background color of the title block, by default has no color

    style : str, optional
        The style of the title block, by default has no style
    """
    message_str: str = __to_string(*message)
    del_lvl()
    println(
        f'{__END_LANGS[lang.lang()]} {message_str.upper()}',
        color=color,
        bg_color=bg_color,
        style=style
    )
    new_line()


def warning(
        *message: Any,
        color: str = 'YELLOW',
        bg_color: str = '',
        style: str = 'bold'
    ) -> None:
    """
    Warning message starts with 'warning: {message}'

    Parameters
    ----------
    message : Any
        The message to display in the log

    color : str, optional
        The color of the message, by default YELLOW

    bg_color : str, optional
        The background color of the message, by default has no color

    style : str, optional
        The style of the message, by default has no style
    """
    message_str: str = __to_string(*message)
    println(f'warning: {message_str}', color=color, bg_color=bg_color, style=style)


def error(
        *message: Any,
        color: str = 'RED',
        bg_color: str = '',
        style: str = 'bold'
    ) -> None:
    """
    Error message is displayed like `error: >>> {message} <<<`

    Parameters
    ----------
    message : Any
        The message to display in the log

    color : str, optional
        The color of the message, by default RED

    bg_color : str, optional
        The background color of the message, by default has no color

    style : str, optional
        The style of the message, by default has no style
    """
    message_str: str = __to_string(*message)
    println(
        f'error: >>> {message_str} <<<',
        color=color,
        bg_color=bg_color,
        style=style
    )


def new_line():
    """
    Display a blank line in the console
    """
    println('', withlvl=False)


def line(
        line_style: str = term.Line.SH,
        size: int = 80,
        **kwargs
    ) -> None:
    """
    Display a line in the console like this `────────────────────`
    whit the indicated size

    Parameters
    ----------
    line_style : str, optional
        The style of the line, by default is `term.Line.SH`

    size : int, optional
        The size of the line to display, by display 30

    kwargs : dict
        The same parameters of the `println` function
    """
    full_line: str = line_style * size

    if full_line[:-1] == ' ':
        full_line = full_line[:-1]

    println(full_line, **kwargs)


def __max_len_value(matrix, nan_format) -> int:
    """
    The function calculates the maximum length of a value in a matrix, replacing NaN values with a
    specified format.

    Parameters
    ----------
    matrix : List[List[Any]]
        a 2D matrix (list of lists) containing values to be checked for maximum length

    nan_format : str
        The string format to use when a cell in the matrix is a NaN value

    Returns
    -------
    int
        an integer value which represents the maximum length of a value in a given matrix.
    """

    def max_value(cell) -> int:
        cellstr = str(cell)
        if cellstr in ('None', 'nan', 'NaN'):
            cellstr = nan_format
        return max(max_len, len(cellstr))

    max_len = 0
    for row in matrix:
        if isinstance(row, list):
            for col in row:
                max_len = max_value(col)
        else:
            max_len = max_value(row)
    return max_len


def __print_matrix_header(
        header: List[str],
        len_index: int,
        color_index: str,
        extra_spacing: str,
        withlvl: bool,
        max_len_value: int,
        lvl_space: int = 3
    ) -> None:
    """
    Print the header of the matrix

    Parameters
    ----------
    header : List[str]
        If the matrix has a header to print with them, by default None

    len_index : int
        Longest value size index of the indexes

    color_index : str
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available

    extra_spacing : str
        The extra spacing befote printing the header

    withlvl : bool
        True if the matrix should be printed with the current indentation False in otherwise

    max_len_value : int
        Longest value size in the matrix

    lvl_space : int
        Number of aditional spaces based on the style
    """
    spaces: str = ' ' * (len_index + lvl_space)
    indentation: str = _ConsoleConfig.indentation_lvl() if withlvl else ''

    println(f'{indentation}{spaces}{extra_spacing}', end='', withlvl=False)
    for i, h in enumerate(header):
        width = max_len_value if isinstance(max_len_value, int) else max_len_value[i]

        println(f' {h : ^{width}} ', color=color_index, end='', withlvl=False)
    new_line()


def __print_matrix_row(
        row: list,
        max_len_value: int,
        color: str,
        nan_format: str,
        color_style: str,
        color_index: str,
        end_line: str,
        start_line: str,
        index_name: str,
        indentation: str
    ) -> None:
    """
    Printed the row of the matrix.

    Parameters
    ----------
    row : list
        The row of the matrix to be printed

    max_len_value : int
        Longest value size in the matrix

    color : str
        The color of the matrix items, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available

    nan_format : str
        The formatted string to print a NaN/None value

    color_style : str
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available

    color_index : str
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available

    end_line : str
        The end of line to be printed

    start_line : str
        The beginning of line to be printed

    index_name : str
        The name of the index to be printed

    indentation : str
        The indentation of the line
    """
    println(indentation, end='', withlvl=False)
    println(index_name,  end='', color=color_index, withlvl=False)
    println(start_line,  end='', color=color_style, withlvl=False)

    for i, cell in enumerate(row):
        cellstr = str(cell) if str(cell) not in ('None', 'nan', 'NaN', '') else nan_format

        width = max_len_value if isinstance(max_len_value, int) else max_len_value[i]
        println(f' {cellstr : ^{width}} ', color=color, end='', withlvl=False)
    println(end_line, color=color_style, withlvl=False)


def __print_matrix_base(
        matrix,
        header: List[str],
        indexes: Union[List[str], str],
        nan_format: str,
        color: str,
        color_index: str,
        color_style: str,
        max_len_value: int,
        len_index: int,
        style : str,
        withlvl: bool,
        start_line: str,
        end_line: str,
        top_line: str,
        bottom_line: str | None,
        middle_vertical_line: str | None,
        middle_horizontal_line: str | None,
        level_space: int = 3
    ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise

    start_line : str
        The beginning of line to be printed

    end_line : str
        The end of line to be printed

    top_line : str, optional
        The top line of the matrix

    bottom_line : str, optional
        The bottom line of the matrix

    middle_vertical_line : str, optional
        The middle vertical line of the matrix

    middle_horizontal_line : str, optional
        The middle horizontal line of the matrix

    level_space : int, optional
        The space between the level and the matrix, by default 3
    """
    indentation: str = _ConsoleConfig.indentation_lvl() if withlvl else ''

    if header:
        __print_matrix_header(header=header,
                              len_index=len_index,
                              color_index=color_index,
                              extra_spacing='',
                              withlvl=withlvl,
                              max_len_value=max_len_value,
                              lvl_space=level_space
                              )

    if top_line is not None and top_line != '':
        println(top_line, color=color_style, withlvl=False)

    for index_row_id, row in enumerate(matrix):
        __print_matrix_row(row = row,
                           max_len_value = max_len_value,
                           color = color,
                           nan_format = nan_format,
                           color_style = color_style,
                           color_index = color_index,
                           end_line = end_line,
                           start_line = start_line,
                           index_name = f'{indexes[index_row_id]: >{len_index}}'
                                        if indexes is not None
                                        else '',
                           indentation = indentation
                           )

    if bottom_line is not None and bottom_line != '':
        println(bottom_line, color=color_style, withlvl=False)


def __print_matrix_box_style(
        matrix,
        header: List[str],
        indexes: Union[List[str], str],
        nan_format: str,
        color: str,
        color_index: str,
        color_style: str,
        max_len_value: int,
        len_index: int,
        style : str,
        withlvl: bool
    ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    try:
        len_matrix = len(matrix[0])
    except:
        len_matrix = len(header)
    div: str = __define_divider_line('-', max_len_value, len_matrix)
    spaces: str = ' ' * (len_index + 3)
    indentation: str = _ConsoleConfig.indentation_lvl() if withlvl else ''

    __print_matrix_base(
        matrix=matrix,
        header=header,
        indexes=indexes,
        nan_format=nan_format,
        color=color,
        color_index=color_index,
        color_style=color_style,
        max_len_value=max_len_value,
        len_index=len_index,
        style=style,
        withlvl=withlvl,
        start_line=' | ',
        end_line=' |' if style == 'box' else '',
        top_line=f'{indentation}{spaces}{div}',
        bottom_line=f'{indentation}{spaces}{div}' if style == 'box' else new_line(),
        middle_vertical_line=None,
        middle_horizontal_line=None
    )


def __print_matrix_numpy_style(
        matrix,
        header: List[str],
        indexes: Union[List[str], str],
        style: str,
        nan_format: str,
        color: str,
        color_index: str,
        color_style: str,
        max_len_value: int,
        len_index: int,
        withlvl: bool
    ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    indentation: str = _ConsoleConfig.indentation_lvl() if withlvl else ''

    if header is not None:
        __print_matrix_header(header = header,
                              len_index = len_index,
                              color_index = color_index,
                              extra_spacing = '   ',
                              withlvl = withlvl,
                              max_len_value = max_len_value
                              )

    max_rows: int = len(matrix)

    for index_row_id, row in enumerate(matrix):
        # string line
        if index_row_id == 0:
            println(indentation, '[ ', end='', color=color_style, withlvl=False)
        else:
            println('  ', indentation, end='', withlvl=False)

        __print_matrix_row(
            row = row,
            max_len_value = max_len_value,
            color = color,
            nan_format = nan_format,
            color_style = color_style,
            color_index = color_index,
            end_line = ' ]' if max_rows != index_row_id + 1 else ' ]  ]',
            start_line = ' [ ',
            index_name = f'{indexes[index_row_id]: >{len_index}}' if indexes is not None else '',
            indentation = indentation
        )


def __print_matrix_without_style(
        matrix,
        header: List[str],
        indexes: Union[List[str], str],
        style: str,
        nan_format: str,
        color: str,
        color_index: str,
        color_style: str,
        max_len_value: int,
        len_index: int,
        withlvl: bool
    ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    __print_matrix_base(
        matrix=matrix,
        header=header,
        indexes=indexes,
        nan_format=nan_format,
        color=color,
        color_index=color_index,
        color_style=color_style,
        max_len_value=max_len_value,
        len_index=len_index,
        style=style,
        withlvl=withlvl,
        start_line='',
        end_line='',
        top_line='',
        bottom_line='',
        middle_vertical_line=None,
        middle_horizontal_line=None,
        level_space=0
    )


def __define_divider_line(style: str, max_len_value: int | list, len_matrix: int) -> str:
    """
    Define the divider line for the matrix

    Parameters
    ----------
    style : str
        The style of the divider line

    max_len_value : int | list
        The longest value in the matrix

    len_matrix : int
        The number of columns in the matrix

    Returns
    -------
    str
        The divider line
    """
    if isinstance(max_len_value, list):
        width: int = sum(w for w in max_len_value)
    else:
        width: int = max_len_value * (len_matrix - 1)
    div: str = style * width + style * (len_matrix * 2)
    return div


def __print_matrix_simpleline_style(
        matrix,
        header: List[str],
        indexes: Union[List[str], str],
        nan_format: str,
        color: str,
        color_index: str,
        color_style: str,
        max_len_value: int,
        len_index: int,
        style : str,
        withlvl: bool
    ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    try:
        len_matrix: int = len(matrix[0])
    except:
        len_matrix: int = len(header)
    div: str = __define_divider_line(term.Line.SH, max_len_value, len_matrix + 1)
    spaces: str = ' ' * (len_index + 1)
    indentation: str = _ConsoleConfig.indentation_lvl() if withlvl else ''

    __print_matrix_base(
        matrix=matrix,
        header=header,
        indexes=indexes,
        nan_format=nan_format,
        color=color,
        color_index=color_index,
        color_style=color_style,
        max_len_value=max_len_value,
        len_index=len_index,
        style=style,
        withlvl=withlvl,
        start_line=f' {term.Line.SV} ',
        end_line=f' {term.Line.SV} ',
        top_line=f'{indentation}{spaces}{term.Line.STL}{div}{term.Line.STR}',
        bottom_line=f'{indentation}{spaces}{term.Line.SBL}{div}{term.Line.SBR}',
        middle_vertical_line=None,
        middle_horizontal_line=None
    )


def __print_matrix_doubleline_style(matrix,
                                    header: List[str],
                                    indexes: Union[List[str], str],
                                    nan_format: str,
                                    color: str,
                                    color_index: str,
                                    color_style: str,
                                    max_len_value: int,
                                    len_index: int,
                                    style : str,
                                    withlvl: bool
                                    ) -> None:
    """
    The matrix has been printed in a box or semibox style.

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str], optional
        If the matrix has a header to print with them, by default None

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name,
        - `all` to show number index for row and columns, only show the index for columns if the
        header are empty (`None`)
        - `row` to show the index of the row,
        - `col` to show the index of the column
        - `None` do not show any index, by default `all`

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    max_len_value : int
        Longest value of the array

    len_index : int
        Longest index of the array

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise
    """
    try:
        len_matrix: int = len(matrix[0])
    except:
        len_matrix: int = len(header)
    div: str = __define_divider_line(term.Line.DH, max_len_value, len_matrix + 1)
    spaces: str = ' ' * (len_index + 1)
    indentation: str = _ConsoleConfig.indentation_lvl() if withlvl else ''

    __print_matrix_base(
        matrix=matrix,
        header=header,
        indexes=indexes,
        nan_format=nan_format,
        color=color,
        color_index=color_index,
        color_style=color_style,
        max_len_value=max_len_value,
        len_index=len_index,
        style=style,
        withlvl=withlvl,
        start_line=f' {term.Line.DV} ',
        end_line=f' {term.Line.DV} ',
        top_line=f'{indentation}{spaces}{term.Line.DTL}{div}{term.Line.DTR}',
        bottom_line=f'{indentation}{spaces}{term.Line.DBL}{div}{term.Line.DBR}',
        middle_vertical_line=None,
        middle_horizontal_line=None
    )


def print_title(
        *message: Any,
        color: str | None = None,
        bg_color: str | None = None,
        style: str | None = None,
        align: str = 'center',
        total_space: int = 30
    ) -> None:
    """
    Display a title in the console

    Parameters
    ----------
    message : Any
        The title of the block

    color : str, optional
        The color of the title block, by default BLUE

    bg_color : str, optional
        The background color of the title block, by default has no color

    style : str, optional
        The style of the title block, by default has no style

    align : str, optional
        The alignment of the title, by default `center`
        - `center` or `c` The title is centered
        - `left` or `l` The title is aligned to the left
        - `right` or `r` The title is aligned to the right

    num_values : int, optional
        The number of values to be displayed, by default 30
    """
    message_str: str = __to_string(*message)

    new_line()

    if message_str:
        if align in ('center', 'c'):
            message_str = message_str.center(total_space)
        elif align in ('left', 'l'):
            message_str = message_str.ljust(total_space)
        elif align in ('right', 'r'):
            message_str = message_str.rjust(total_space)

        println(message, color=color, style=style, bg_color=bg_color)
        new_line()

# TODO: Add support for alignment center, left and right for the values
def print_matrix(
        matrix,
        header: Union[List[str], str] = 'all',
        indexes: Union[List[str], str] = 'all',
        style: str = 'box',
        nan_format: str = '',
        color: str | None = None,
        color_index: str = '',
        color_style: str = '',
        withlvl: bool = True,
        column_width: str = 'auto',
        title: str | None = None,
        title_color: str | None = None,
        title_bg_color: str | None = None,
        title_style: str | None = None,
        title_align: str = 'center',
    ) -> None:
    """
    Print a matrix in a pretty formatted

    >>> matrix = [[1, 2, 3], [4, 5, 6]]
    >>> print_matrix(matrix)
    ...
    ...     0  1  2
    ...     -------
    ... 0 | 1  2  3 |
    ... 1 | 4  5  6 |
    ...     -------

    >>> print_matrix(matrix,
    >>>              header=['one', 'two', 'three'],
    >>>              indexes=['row1', 'row2'],
    >>>              style='semibox'
    >>>              )
    ...
    ...          one     two    three
    ...        -----------------------
    ... row1 |    1       2       3
    ... row2 |    4       5       6

    Parameters
    ----------
    matrix : Iterable object
        An iterable object to print

    header : List[str] | str, optional
        A list of strings if is a presonalized column name
        - `all` to show the index of the column,
        - `None` do not show any index, by default `all`

    indexes : List[str] | str, optional
        A list of strings if is a presonalized index name
        - `all` to show the index of the row,
        - `None` do not show any index, by default `all`

    style : str, optional
        The style to print the matrix, by default `box`
        - `box` Borders around the matrix
        - `semibox` Borders at the top and left of the matrix
        - `numpy` or `np` Has been printed like a NumPy matrix
        - `simpleline` or `line` or `sl` Only the grid lines of the matrix based on single lines of
           term.emojis.Line
        - `doubleline` or `dl` Only the grid lines of the matrix based on double lines of
           term.emojis.Line
        - `None` Without borders, only show the values

    nan_format : str, optional
        The formatted string to print a NaN/None value, by default ''

    color : str, optional
        The color of the matrix items, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_index : str, optional
        The color of the index, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    color_style : str, optional
        The color style to print the matrix, for example the grid lines,
        the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    withlvl : bool, optional
        True if the matrix should be printed with the current indentation False in otherwise

    column_width : str, optional
        The width of the columns, by default `auto`
        - `auto` The width of the columns is the longest value of the column
        - `equal` The width of the columns is the same

    title : str, optional
        The title of the matrix, by default has no title

    title_color : str, optional
        The color of the title, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available

    title_bg_color : str, optional
        The background color of the title, the color must be one of the `console.ColorBackground()`
        or `console.ColorText()` for all colors available

    title_style : str, optional
        The style of the title, the style must be one of the `console.StyleText()`

    title_align : str, optional
        The alignment of the title, by default `center`

    Raises
    ------
    ErrorNotDefinedStyle
        If the style is not defined
    """
    if indexes == 'all':
        indexes: list[str] = [str(i) for i in range(len(matrix))]

    if header == 'all':
        header: list[str] = [str(i) for i in range(len(matrix[0]))]

    if column_width == 'equal':
        max_len_value: int = __max_len_value(matrix, nan_format)
        max_len_value: int = max(
            max_len_value,
            __max_len_value([] if header is None else header, nan_format)
        )
    else:
        matrix_with_header = [header] + matrix
        matrix_by_column = list(zip(*matrix_with_header))
        max_len_value = [__max_len_value(column, nan_format) for column in matrix_by_column]

    if title:
        space = max([len(str(i)) for i in indexes]) + sum(len(str(i)) + 3 for i in header) + 2
        print_title(
            title,
            color=title_color,
            bg_color=title_bg_color,
            style=title_style,
            align=title_align,
            total_space=space
        )

    len_index = 0

    if isinstance(indexes, list):
        len_index: int = __max_len_value(indexes, nan_format)

    kwargs = {
        'matrix' : matrix,
        'header' : header,
        'indexes' : indexes,
        'nan_format' : nan_format,
        'color' : color,
        'color_index' : color_index,
        'color_style' : color_style,
        'max_len_value' : max_len_value,
        'len_index' : len_index,
        'style' : style,
        'withlvl' : withlvl
    }

    if style is None:
        __print_matrix_without_style(**kwargs)
    elif style in ('box', 'semibox'):
        __print_matrix_box_style(**kwargs)
    elif style in ('numpy', 'np'):
        __print_matrix_numpy_style(**kwargs)
    elif style in ('simpleline', 'sl', 'line'):
        __print_matrix_simpleline_style(**kwargs)
    elif style in ('doubleline', 'dl'):
        __print_matrix_doubleline_style(**kwargs)
    else:
        raise ex.ErrorNotDefinedStyle(style)


def inputln(
        *message: Any,
        endl: str = '',
        input_type: type = str,
        withlvl: bool = True,
        color: str = '',
        bg_color: str = '',
        reset_all_colors: bool = True,
        style: str = '',
        sep: str = ' '
    ) -> None:
    """
    A utility function that prompts the user to input data from the console,
    with support for customization of the prompt message appearance.


    Parameters
    ----------
    message : Any
        Message to print to console

    endl : str, optional
        The end of the message, by default is empty

    input_type : type, optional
        The type of the input, by default `str`. This parameter specifies
        the type of the returned user input value.

    withlvl : bool, optional
        True if the message should be printed with the current indentation
        False is not necessary, by default `True`

    color : str, optional
        The color of the message, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    bg_color : str, optional
        The background color of the message, the color must be one of the `console.ColorBackground()`
        or `console.ColorText()` for all colors available; by default has no color

    reset_all_colors : bool, optional
        True to reset all colors, False is not necessary, by default `True`

    style : str, optional
        The style of the message, the style must be one of the `console.StyleText()`,
        by default has no style

    sep : str, optional
        The separator between the values, by default is a space
    """
    println(
        *message,
        end=endl,
        withlvl=withlvl,
        color=color,
        bg_color=bg_color,
        reset_all_colors=reset_all_colors,
        style=style,
        sep=sep
    )

    return input_type(builtins.input())


def textbox(
        *message: Any,
        withlvl: bool = True,
        color: str = '',
        bg_color: str = '',
        reset_all_colors: bool = True,
        style: str = '',
        sep: str = ' ',
        border: str | dict | None = 'simpleline',
        border_color: str = '',
        border_style: str = '',
        allow_empty: bool = False,
        text_align: str = 'left'
    ) -> None:
    """
    Print the message to the console, the `endl` is the same as `end` in print function
    and is necessary print the message with the current indentation level and the color
    indicate.

    Parameters
    ----------
    message : Any
        Message to print to console

    withlvl : bool, optional
        True if the message should be printed with the current indentation
        False is not necessary, by default `True`

    color : str, optional
        The color of the message, the color must be one of the `console.ColorText()`
        ['RED', 'GREEN', ...], `console.ColorText()` for all colors available;
        by default has no color

    bg_color : str, optional
        The background color of the message, the color must be one of the `console.ColorBackground()`
        or `console.ColorText()` for all colors available; by default has no color

    reset_all_colors : bool, optional
        True to reset all colors, False is not necessary, by default `True`

    style : str, optional
        The style of the message, the style must be one of the `console.StyleText()`,
        by default has no style

    sep : str, optional
        The separator between the values, by default is a space

    border : str | dict, optional
        The style of the border, the style must be one of the if is a string
        `['simpleline', `sl`, 'doubleline', `dl`]`, by default is `simpleline`
        - `simpleline` or `sl` The border is a simple line
        - `doubleline` or `dl` The border is a double line
        If is a dictionary, the dictionary must have the following keys
        - `top_left` The top border left
        - `top_right` The top border right
        - `bottom_left` The bottom border left
        - `bottom_right` The bottom border right
        - `vertical` The vertical border
        - `horizontal` The horizontal border

    border_color : str, optional
        The color of the border, the color must be one of the `console.ColorText()`

    border_style : str, optional
        The style of the border, the style must be one of the `console.StyleText()`

    allow_empty : bool, optional
        True to allow blank lines, at the beginning and end of the message, by default `True`

    text_align : str, optional
        The alignment of the text, by default `left`
        - `center` or `c` The text is centered
        - `left` or `l` The text is aligned to the left
        - `right` or `r` The text is aligned to the right

    Raises
    ------
    ErrorNotDefinedStyle
        If the style is not defined

    Examples
    --------
    >>> textbox('ConsoleVerse', border='doubleline', allow_empty=True)
    ... ╔══════════════╗
    ... ║              ║
    ... ║ ConsoleVerse ║
    ... ║              ║
    ... ╚══════════════╝

    >>> textbox('ConsoleVerse', border='simpleline')
    ... ┌──────────────┐
    ... │ ConsoleVerse │
    ... └──────────────┘
    """
    pln = lambda s: println(s, withlvl=withlvl, color=border_color, style=border_style)

    _bs = {
        'simpleline': {
            'top_left': term.Line.STL,
            'top_right': term.Line.STR,
            'bottom_left': term.Line.SBL,
            'bottom_right': term.Line.SBR,
            'vertical': term.Line.SV,
            'horizontal': term.Line.SH,
        },
        'doubleline': {
            'top_left': term.Line.DTL,
            'top_right': term.Line.DTR,
            'bottom_left': term.Line.DBL,
            'bottom_right': term.Line.DBR,
            'vertical': term.Line.DV,
            'horizontal': term.Line.DH,
        }
    }

    message_str: str = __to_string(*message, sep=sep)
    lines = message_str.split('\n')
    max_len = max([len(l) for l in lines])
    bname = ''

    if isinstance(border, dict):
        _bs['custom'] = border
        bname = 'custom'

    elif isinstance(border, str):
        if border in ('simpleline', 'sl'):
            bname = 'simpleline'
        elif border in ('doubleline', 'dl'):
            bname = 'doubleline'

    if bname == '':
        raise ex.ErrorNotDefinedStyle(border)

    horizontal = _bs[bname]['horizontal'] * (max_len + 2)
    top = _bs[bname]['top_left'] + horizontal + _bs[bname]['top_right']
    bottom = _bs[bname]['bottom_left'] + horizontal + _bs[bname]['bottom_right']
    vertical = _bs[bname]['vertical']
    vertical_blank = vertical + ' ' * (max_len + 2) + vertical

    pln(top)
    if allow_empty:
        pln(vertical_blank)

    for l in lines:
        alignments = {
            'c': '^',
            'r': '>',
            'l': '<',
            'center': '^',
            'right': '>',
            'left': '<',
        }

        align_line = f' {l:{alignments.get(text_align, "<")}{max_len}} '

        println(vertical, withlvl=withlvl, color=border_color, style=border_style, end='')
        println(
            align_line,
            withlvl=False,
            color=color,
            bg_color=bg_color,
            reset_all_colors=reset_all_colors,
            style=style,
            end=''
        )
        println(vertical, withlvl=False, color=border_color, style=border_style)

    if allow_empty:
        pln(vertical_blank)
    pln(bottom)


def progress_bar(
        progress: float,
        width: int = 50,
        bar: str = '#',
        start_bar: str = '[',
        end_bar: str = ']',
        spacing: str = '.',
        pct: bool = True,
        **kwargs
    ) -> None:
    """
    Print a progress bar to the console.

    Parameters
    ----------
    progress : float
        The progress of the bar, the value must be between 0 and 1

    width : int, optional
        The width of the bar, by default is 50

    bar : str, optional
        The character to use for the bar, by default is `#`

    start_bar : str, optional
        The character to use for the start of the bar, by default is `[`

    end_bar : str, optional
        The character to use for the end of the bar, by default is `]`

    spacing : str, optional
        The character to use for the spacing, by default is `.`

    pct : bool, optional
        True to print the percentage, False otherwise, by default is `True`

    Raises
    ------
    ValueError
        If the progress is not between 0 and 1
        If the width is less than 0
        If the bar is not a single character
        If the start_bar is not a single character
        If the end_bar is not a single character

    Examples
    --------
    >>> progress_bar(0.5)
    ... [######.........................] (50%)

    >>> progress_bar(0.5, width=20, bar='=', start_bar='|', end_bar='|', spacing='-', pct=False)
    ... |====================----------|
    """

    if progress < 0 or progress > 1:
        raise ValueError('The progress must be between 0 and 1')

    if width < 0:
        raise ValueError('The width must be greater than 0')

    if len(bar) != 1:
        raise ValueError('The bar must be a single character')

    if len(start_bar) != 1:
        raise ValueError('The start_bar must be a single character')

    if len(end_bar) != 1:
        raise ValueError('The end_bar must be a single character')

    progressing_bar: int = int(progress * width)
    pct_bar: str = ' (' + str(int(progress * 100)) + '%)' if pct else ''

    println(
        start_bar + bar * progressing_bar + spacing * (width - progressing_bar) + end_bar + pct_bar,
        **kwargs
    )


def print_tree(
        tree: dict,
        style_tree: str = 'simple',
        color_tree: str = '',
        **println_options
    ) -> None:
    """
    Print a tree to the console in a tree style.

    Parameters
    ----------
    dictionary : dict
        The dictionary to print

    style_dict : str, optional
        The style of the dictionary, the style must be one of the `console.StyleText()`,
        by default is `simple`

    Examples
    --------
    >>> print_tree({'a': 1, 'b': 2, 'c': 3})
    ... ┌─ a
    ... │  └─ 1
    ... ├─ b
    ... │  └─ 2
    ... └─ c
    ...    └─ 3

    >>> print_tree({'a': 1, 'b': {'a': 1, 'b': 2}, 'c': 3}, style_dict='doubleline')
    ... ╔═ a
    ... ║  ╚═ 1
    ... ╠═ b
    ... ║  ╠═ a
    ... ║  ║  ╚═ 1
    ... ║  ╚═ b
    ... ║     ╚═ 2
    ... ╚═ c
    ...    ╚═ 3
    """
    STYLE_TREE = {
        'simple': {
            'upper_left': term.Line.STL,
            'down_left': term.Line.SBL,
            'vertical': term.Line.SV,
            'horizontal': term.Line.SH,
            'vertical_and_right': term.Line.SL
        },
        'doubleline': {
            'upper_left': term.Line.DTL,
            'down_left': term.Line.DBL,
            'vertical': term.Line.DV,
            'horizontal': term.Line.DH,
            'vertical_and_right': term.Line.DL
        }
    }
    style = STYLE_TREE.get(style_tree)
    if style is None:
        raise ex.ErrorNotDefinedStyle(style_tree)

    upper_left = style['upper_left']
    down_left = style['down_left']
    vertical = style['vertical']
    horizontal = style['horizontal']
    vertical_and_right = style['vertical_and_right']

    def recursive_print_tree(
            sub_tree: dict,
            level: int = 0,
            start_bar: str = ''
        ):
        """
        Print a tree to the console in a tree style.

        Parameters
        ----------
        sub_tree : dict
            The dictionary to print

        level : int, optional
            The level of the tree, by default is 0

        start_bar : str, optional
            The start bar of the tree, by default is ''
        """
        len_sub_tree = len(sub_tree)
        for i, (k, v) in enumerate(sub_tree.items()):
            bar_line = ''
            if   i == 0 and level != 0 and len_sub_tree > 1:
                bar_line = f'{vertical_and_right}{horizontal}'
            elif i == 0 and level == 0 and len_sub_tree > 1 :
                bar_line = f'{upper_left}{horizontal}'
            elif i == 0 and len_sub_tree == 1:
                bar_line = f'{down_left}{horizontal}'
            elif i == len_sub_tree - 1:
                bar_line = f'{down_left}{horizontal}'
            else:
                bar_line = f'{vertical_and_right}{horizontal}'

            println(f'{start_bar}{bar_line}', color=color_tree, end=' ')
            println(k, **println_options)

            if isinstance(v, dict):
                if i == len_sub_tree - 1:
                    new_start_bar = f'{start_bar}  '
                else:
                    new_start_bar = f'{start_bar}{vertical}  '
                recursive_print_tree(v, level + 1, start_bar=new_start_bar)
            else:
                last_lvl = ' ' if i == len_sub_tree - 1 else vertical
                bar_line = f'{start_bar}{last_lvl}  {down_left}{horizontal}'
                println(bar_line, color=color_tree, end=' ')
                println(v, **println_options)

    recursive_print_tree(tree)


def bar_chart(
        data: list[int] | dict,
        colors: list[str],
        bar: str = '███',
        title: str = '',
        title_color: str = '',
        title_style: str = '',
        title_bg_color: str = '',
        title_align: str = 'center',
    ) -> None:
    """
    Print a bar chart to the console.

    Parameters
    ----------
    data : Union(list[int], dict)
        The data to print

    colors : list[str]
        The colors of the bars

    bar : str, optional
        The bar to print, by default is '███'

    title : str, optional
        The title of the bar chart, by default is empty

    title_color : str, optional
        The color of the title, by default has no color

    title_style : str, optional
        The style of the title, by default has no style

    title_bg_color : str, optional
        The background color of the title, by default has no background color

    title_align : str, optional
        The align of the title, by default is 'center', the options are
        - `center` The title is centered
        - `left` The title is aligned to the left
        - `right` The title is aligned to the right

    """

    def normalize(value: int) -> int:
        return int(value / max(data) * 10)

    def colorize(text: str, color: str) -> str:
        return _colorize(text, color=color, style='', bg_color='', reset_console_colors=True)

    data_norm = [normalize(value) for value in data]

    max_value = max(data_norm)
    num_values = len(data)
    bar = f'{bar} '
    len_bar = len(bar)

    new_line()
    print_title(
        title,
        color=title_color,
        style=title_style,
        bg_color=title_bg_color,
        align=title_align,
        total_space=num_values * len_bar
    )

    for i in range(max_value, 0, -1):
        chart_line = ''
        for j, value in enumerate(data_norm):
            if value >= i:
                chart_line += colorize(bar, colors[j])
            else:
                chart_line += ' ' * len_bar
        println(chart_line)

    line(size=num_values * len_bar)
    println(
        ' '.join(
            colorize(
                str(value).center(len_bar - 1), colors[i]
            )
            for i, value in enumerate(data)
        )
    )

    new_line()
