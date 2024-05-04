"""
A test case for the console module.

This test case verifies the behavior of the console module by comparing
the output of console.println() with the standard print() function.
"""

import unittest
from unittest.mock import patch
from consoleverse import console


class TestConsolePrintln(unittest.TestCase):
    """
    A test case for the console module.

    This test case verifies the behavior of the console module by comparing
    the output of console.println() with the standard print() function.
    """

    def test_println_vs_python_print(self):
        """
        Test that console.println() produces the same output as print().

        This test verifies that the output of console.println() matches the
        output of the print() function in the same conditions, with the same arguments.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', withlvl=False)
            mock_print.assert_called_once_with('Hello ConsoleVerse!\x1b[0m', end='\n')

    def test_println_vs_python_print_with_end_delimiter(self):
        """
        Test that console.println() with end delimiter produces the same output as print().

        This test verifies that the output of console.println() with a specified end
        delimiter matches the output of the print() function with the same end delimiter.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', endl=' ')
            mock_print.assert_called_once_with('Hello ConsoleVerse!\x1b[0m', end=' ')

    def test_println_vs_python_print_with_several_args(self):
        """
        Test that console.println() with multiple arguments produces the same output as print().

        This test verifies that the output of console.println() with multiple arguments
        matches the output of the print() function with the same arguments.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', 'Hello ConsoleVerse!', 'Hello ConsoleVerse!')
            mock_print.assert_called_once_with('Hello ConsoleVerse! Hello ConsoleVerse! Hello ConsoleVerse!\x1b[0m', end='\n')

    def test_println_vs_python_print_with_several_args_and_separator(self):
        """
        Test that console.println() with multiple arguments and a separator produces
        the same output as print().
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', 'Hello ConsoleVerse!', 'Hello ConsoleVerse!', sep='~')
            mock_print.assert_called_once_with('Hello ConsoleVerse!~Hello ConsoleVerse!~Hello ConsoleVerse!\x1b[0m', end='\n')

    def test_println_vs_python_print_with_several_args_and_separator_and_end_delimiter(self):
        """
        Test that console.println() with multiple arguments, a separator and an end delimiter
        produces the same output as print().
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', 'Hello ConsoleVerse!', 'Hello ConsoleVerse!', sep='~', endl=' ')
            mock_print.assert_called_once_with('Hello ConsoleVerse!~Hello ConsoleVerse!~Hello ConsoleVerse!\x1b[0m', end=' ')

    def test_println_vs_python_color_print(self):
        """
        Test that console.println() with a color argument produces the same output as print().

        This test verifies that the output of console.println() with a color argument
        matches the output of the print() function with the same color argument.
        """

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK')
            mock_print.assert_called_once_with('\033[30mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='RED')
            mock_print.assert_called_once_with('\033[31mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='GREEN')
            mock_print.assert_called_once_with('\033[32mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='YELLOW')
            mock_print.assert_called_once_with('\033[33mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLUE')
            mock_print.assert_called_once_with('\033[34mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='MAGENTA')
            mock_print.assert_called_once_with('\033[35mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='CYAN')
            mock_print.assert_called_once_with('\033[36mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='WHITE')
            mock_print.assert_called_once_with('\033[37mHello ConsoleVerse!\x1b[0m', end='\n')

    def test_println_vs_python_bg_color_print(self):
        """
        Test that console.println() with a background color argument produces the same output as print().

        This test verifies that the output of console.println() with a background color argument
        matches the output of the print() function with the same background color argument.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='BLACK')
            mock_print.assert_called_once_with('\033[40mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='RED')
            mock_print.assert_called_once_with('\033[41mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='GREEN')
            mock_print.assert_called_once_with('\033[42mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='YELLOW')
            mock_print.assert_called_once_with('\033[43mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='BLUE')
            mock_print.assert_called_once_with('\033[44mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='MAGENTA')
            mock_print.assert_called_once_with('\033[45mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='CYAN')
            mock_print.assert_called_once_with('\033[46mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='WHITE')
            mock_print.assert_called_once_with('\033[47mHello ConsoleVerse!\x1b[0m', end='\n')

    def test_println_vs_python_style_print(self):
        """
        Test that console.println() with a style argument produces the same output as print().

        This test verifies that the output of console.println() with a style argument
        matches the output of the print() function with the same style argument.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', style='BOLD')
            mock_print.assert_called_once_with('\033[1mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', style='DIM')
            mock_print.assert_called_once_with('\033[2mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', style='UNDERLINE')
            mock_print.assert_called_once_with('\033[4mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', style='BLINK')
            mock_print.assert_called_once_with('\033[5mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', style='REVERSE')
            mock_print.assert_called_once_with('\033[7mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', style='HIDDEN')
            mock_print.assert_called_once_with('\033[8mHello ConsoleVerse!\x1b[0m', end='\n')

    @unittest.skip('Fix console.println() to support color with bg_color and style.')
    def test_println_vs_python_color_bg_color_print(self):
        """
        Test that console.println() with a color and background color argument produces the same output as print().

        This test verifies that the output of console.println() with a color and background color argument
        matches the output of the print() function with the same color and background color argument.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='green', bg_color='BLACK')
            mock_print.assert_called_once_with('\033[32;40mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='RED')
            mock_print.assert_called_once_with('\033[30;41mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='GREEN')
            mock_print.assert_called_once_with('\033[30;42mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='YELLOW')
            mock_print.assert_called_once_with('\033[30;43mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='BLUE')
            mock_print.assert_called_once_with('\033[30;44mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='MAGENTA')
            mock_print.assert_called_once_with('\033[30;45mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='CYAN')
            mock_print.assert_called_once_with('\033[30;46mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='WHITE')
            mock_print.assert_called_once_with('\033[30;47mHello ConsoleVerse!\x1b[0m', end='\n')

    @unittest.skip('Fix console.println() to support color with bg_color and style.')
    def test_println_vs_python_color_bg_color_style_print(self):
        """
        Test that console.println() with a color, background color, and style argument produces the same output as print().

        This test verifies that the output of console.println() with a color, background color, and style argument
        matches the output of the print() function with the same color, background color, and style argument.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='GREEN', bg_color='BLACK', style='BOLD')
            mock_print.assert_called_once_with('\033[32;40;1mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='RED', style='DIM')
            mock_print.assert_called_once_with('\033[30;41;2mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='GREEN', style='UNDERLINE')
            mock_print.assert_called_once_with('\033[30;42;4mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='YELLOW', style='BLINK')
            mock_print.assert_called_once_with('\033[30;43;5mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='BLUE', style='REVERSE')
            mock_print.assert_called_once_with('\033[30;44;7mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLACK', bg_color='MAGENTA', style='HIDDEN')
            mock_print.assert_called_once_with('\033[30;45;8mHello ConsoleVerse!\x1b[0m', end='\n')

    @unittest.skip('Fix console.println() to support color with bg_color and style.')
    def test_println_vs_python_color_style_print(self):
        """
        Test that console.println() with a color and style argument produces the same output as print().

        This test verifies that the output of console.println() with a color and style argument
        matches the output of the print() function with the same color and style argument.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='GREEN', style='BOLD')
            mock_print.assert_called_once_with('\033[32;1mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='RED', style='DIM')
            mock_print.assert_called_once_with('\033[31;2mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='MAGENTA', style='UNDERLINE')
            mock_print.assert_called_once_with('\033[35;4mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='YELLOW', style='BLINK')
            mock_print.assert_called_once_with('\033[33;5mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='BLUE', style='REVERSE')
            mock_print.assert_called_once_with('\033[34;7mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', color='CYAN', style='HIDDEN')
            mock_print.assert_called_once_with('\033[36;8mHello ConsoleVerse!\x1b[0m', end='\n')

    @unittest.skip('Fix console.println() to support color with bg_color and style.')
    def test_println_vs_python_bg_color_style_print(self):
        """
        Test that console.println() with a background color and style argument produces the same output as print().

        This test verifies that the output of console.println() with a background color and style argument
        matches the output of the print() function with the same background color and style argument.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='BLACK', style='BOLD')
            mock_print.assert_called_once_with('\033[40;1mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='RED', style='DIM')
            mock_print.assert_called_once_with('\033[41;2mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='GREEN', style='UNDERLINE')
            mock_print.assert_called_once_with('\033[42;4mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='YELLOW', style='BLINK')
            mock_print.assert_called_once_with('\033[43;5mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='BLUE', style='REVERSE')
            mock_print.assert_called_once_with('\033[44;7mHello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello ConsoleVerse!', bg_color='MAGENTA', style='HIDDEN')
            mock_print.assert_called_once_with('\033[45;8mHello ConsoleVerse!\x1b[0m', end='\n')

    def test_println_vs_python_print_separator(self):
        """
        Test that console.println() with a separator argument produces the same output as print().

        This test verifies that the output of console.println() with a separator argument
        matches the output of the print() function with the same separator argument.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!')
            mock_print.assert_called_once_with('Hello ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!', sep='~')
            mock_print.assert_called_once_with('Hello~ConsoleVerse!\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!', sep='~', endl='')
            mock_print.assert_called_once_with('Hello~ConsoleVerse!\x1b[0m', end='')

    def test_println_vs_python_print_list(self):
        """
        Test that console.println() with a list argument produces the same output as print().

        This test verifies that the output of console.println() with a list argument
        matches the output of the print() function with the same list argument.
        """
        with patch('builtins.print') as mock_print:
            console.println(['Hello', 'ConsoleVerse!'])
            mock_print.assert_called_once_with("['Hello', 'ConsoleVerse!']\x1b[0m", end='\n')

    def test_println_vs_python_print_tuple(self):
        """
        Test that console.println() with a tuple argument produces the same output as print().

        This test verifies that the output of console.println() with a tuple argument
        matches the output of the print() function with the same tuple argument.
        """
        with patch('builtins.print') as mock_print:
            console.println(('Hello', 'ConsoleVerse!'))
            mock_print.assert_called_once_with("('Hello', 'ConsoleVerse!')\x1b[0m", end='\n')

    def test_println_vs_python_print_dict(self):
        """
        Test that console.println() with a dict argument produces the same output as print().

        This test verifies that the output of console.println() with a dict argument
        matches the output of the print() function with the same dict argument.
        """
        with patch('builtins.print') as mock_print:
            console.println({'Hello': 'ConsoleVerse!'})
            mock_print.assert_called_once_with("{'Hello': 'ConsoleVerse!'}\x1b[0m", end='\n')

    def test_println_vs_python_print_set(self):
        """
        Test that console.println() with a set argument produces the same output as print().

        This test verifies that the output of console.println() with a set argument
        matches the output of the print() function with the same set argument.
        """
        with patch('builtins.print') as mock_print:
            console.println({'Hello', 'ConsoleVerse!'})
            mock_print.assert_called_once_with("{'Hello', 'ConsoleVerse!'}\x1b[0m", end='\n')

    def test_println_vs_python_print_bool(self):
        """
        Test that console.println() with a bool argument produces the same output as print().

        This test verifies that the output of console.println() with a bool argument
        matches the output of the print() function with the same bool argument.
        """
        with patch('builtins.print') as mock_print:
            console.println(True)
            mock_print.assert_called_once_with('True\x1b[0m', end='\n')

        with patch('builtins.print') as mock_print:
            console.println(False)
            mock_print.assert_called_once_with('False\x1b[0m', end='\n')

    def test_println_vs_python_print_int(self):
        """
        Test that console.println() with an int argument produces the same output as print().

        This test verifies that the output of console.println() with an int argument
        matches the output of the print() function with the same int argument.
        """
        with patch('builtins.print') as mock_print:
            console.println(123)
            mock_print.assert_called_once_with('123\x1b[0m', end='\n')

    def test_println_vs_python_print_float(self):
        """
        Test that console.println() with a float argument produces the same output as print().

        This test verifies that the output of console.println() with a float argument
        matches the output of the print() function with the same float argument.
        """
        with patch('builtins.print') as mock_print:
            console.println(123.456)
            mock_print.assert_called_once_with('123.456\x1b[0m', end='\n')

    def test_println_vs_python_print_none(self):
        """
        Test that console.println() with a None argument produces the same output as print().

        This test verifies that the output of console.println() with a None argument
        matches the output of the print() function with the same None argument.
        """
        with patch('builtins.print') as mock_print:
            console.println(None)
            mock_print.assert_called_once_with('None\x1b[0m', end='\n')

    def test_println_vs_python_print_multiple_args(self):
        """
        Test that console.println() with multiple arguments produces the same output as print().

        This test verifies that the output of console.println() with multiple arguments
        matches the output of the print() function with the same multiple arguments.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!', 123, True, None)
            mock_print.assert_called_once_with('Hello ConsoleVerse! 123 True None\x1b[0m', end='\n')

    def test_println_vs_python_print_multiple_args_separator(self):
        """
        Test that console.println() with multiple arguments and a separator produces the same output as print().

        This test verifies that the output of console.println() with multiple arguments and a separator
        matches the output of the print() function with the same multiple arguments and separator.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!', 123, True, None, sep='~')
            mock_print.assert_called_once_with('Hello~ConsoleVerse!~123~True~None\x1b[0m', end='\n')

    def test_println_vs_python_print_multiple_args_separator_end(self):
        """
        Test that console.println() with multiple arguments, a separator, and an end produces the same output as print().

        This test verifies that the output of console.println() with multiple arguments, a separator, and an end
        matches the output of the print() function with the same multiple arguments, separator, and end.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!', 123, True, None, sep='~', endl='')
            mock_print.assert_called_once_with('Hello~ConsoleVerse!~123~True~None\x1b[0m', end='')

    def test_println_vs_python_print_multiple_args_separator_end_color(self):
        """
        Test that console.println() with multiple arguments, a separator, and an end produces the same output as print().

        This test verifies that the output of console.println() with multiple arguments, a separator, and an end
        matches the output of the print() function with the same multiple arguments, separator, and end.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!', 123, True, None, sep='~', endl='', color='red')
            mock_print.assert_called_once_with('\x1b[31mHello~ConsoleVerse!~123~True~None\x1b[0m', end='')

    @unittest.skip('Fix console.println() to support color with bg_color and style.')
    def test_println_vs_python_print_multiple_args_separator_end_color_bgcolor(self):
        """
        Test that console.println() with multiple arguments, a separator, and an end produces the same output as print().

        This test verifies that the output of console.println() with multiple arguments, a separator, and an end
        matches the output of the print() function with the same multiple arguments, separator, and end.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!', 123, True, None, sep='~', endl='', color='red', bgcolor='blue')
            mock_print.assert_called_once_with('\x1b[31;44mHello~ConsoleVerse!~123~True~None\x1b[0m', end='')

    @unittest.skip('Fix console.println() to support color with bg_color and style.')
    def test_println_vs_python_print_multiple_args_separator_end_color_bgcolor_style(self):
        """
        Test that console.println() with multiple arguments, a separator, and an end produces the same output as print().

        This test verifies that the output of console.println() with multiple arguments, a separator, and an end
        matches the output of the print() function with the same multiple arguments, separator, and end.
        """
        with patch('builtins.print') as mock_print:
            console.println('Hello', 'ConsoleVerse!', 123, True, None, sep='~', endl='', color='red', bgcolor='blue', style='bold')
            mock_print.assert_called_once_with('\x1b[31;44;1mHello~ConsoleVerse!~123~True~None\x1b[0m', end='')

