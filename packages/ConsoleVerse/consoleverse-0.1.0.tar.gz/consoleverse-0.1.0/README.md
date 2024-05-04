# 💻 ConsoleVerse


<center>
<img src="docs/img/ConsoleVerse_logo_fullcolor.png" width="150" style="border-radius: 25%;">

<hr>

[![License](https://img.shields.io/github/license/JuanS3/consoleverse)](https://github.com/JuanS3/consoleverse/blob/main/LICENSE)
[![License](https://img.shields.io/github/languages/code-size/JuanS3/consoleverse?color=green&logo=python)](https://img.shields.io/github/languages/code-size/JuanS3/consoleverse?color=green&logo=python)

</center>



ConsoleVerse is a **Python** library that provides a set of tools for managing console output, input and styling. It aims to simplify console interactions and improve user experience.

## 🚀 Features

- Simple and intuitive library interface
- Customizable styling options
- Support for progress bars
- Cross-platform compatibility

## 💾 Installation

To install ConsoleVerse, simply run:

```python
# from PyPI
pip install consoleverse # is not available yet

# from GitHub
pip install git+https://github.com/JuanS3/ConsoleVerse.git
```


## 📕 Getting Started

To use ConsoleVerse in your Python project, simply import it and start using its features:

```python
>>> from consoleverse import console

>>> console.println("Hello, ConsoleVerse!")
... Hello, ConsoleVerse!

>>> console.inputln("Your name? ")
... Your name?

>>> matrix = [
>>>     [1, 2, 3],
>>>     [4, 5, 6]
>>> ]
>>> print_matrix(matrix)
...
...     0  1  2
...     -------
... 0 | 1  2  3 |
... 1 | 4  5  6 |
...     -------

>>> print_matrix(
>>>     matrix,
>>>     header=['one', 'two', 'three'],
>>>     indexes=['row1', 'row2'],
>>>     style='semibox'
>>> )
...
...          one     two    three
...        -----------------------
... row1 |    1       2       3
... row2 |    4       5       6
```

For more detailed usage instructions, please see the usage documentation.

## 📃 Examples
Check out the [examples directory](examples/) for some sample code demonstrating ConsoleVerse's capabilities.

## 🖐🏻 Contributing
Contributions to ConsoleVerse are welcome and appreciated! Please see the [contribution guidelines](CONTRIBUTING.md) for more information on how to get involved.

## 📜 License
ConsoleVerse is released under the [MIT License](LICENSE). See the [license file](LICENSE) for more information.

## 👏🏻 Credits
ConsoleVerse was developed by [JuanS3](github.com/JuanS3).
