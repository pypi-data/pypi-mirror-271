from consoleverse.config import lang


class ValueErrorConsole(ValueError):...
class ErrorNotDefinedStyle(ValueErrorConsole):
    MSG = {
        lang.Language()['en']: 'The style "{}" is not defined in the consoleverse',
        lang.Language()['es']: 'El estilo "{}" no esta definido en el consoleverse',
    }

    def __init__(self, style: str):
        self.style = style
        super().__init__(self.MSG[lang.lang()].format(style))

    def __repr__(self):
        return f'ErrorNotDefinedStyle({self.style!r})'


class ErrorNotDefinedBorderStyle(ValueErrorConsole):
    MSG = {
        lang.Language()['en']: 'The border style "{}" is not defined in the consoleverse',
        lang.Language()['es']: 'El estilo de borde "{}" no esta definido en el consoleverse',
    }

    def __init__(self, border_style: str):
        self.border_style = border_style
        super().__init__(self.MSG[lang.lang()].format(border_style))

    def __repr__(self):
        return f'ErrorNotDefinedBorderStyle({self.border_style!r})'


class ErrorNotDefinedColor(ValueErrorConsole):
    MSG = {
        lang.Language()['en']: 'The color "{}" is not defined in the consoleverse',
        lang.Language()['es']: 'El color "{}" no esta definido en el consoleverse',
    }

    def __init__(self, color: str):
        self.color = color
        super().__init__(self.MSG[lang.lang()].format(color))

    def __repr__(self):
        return f'ErrorNotDefinedColor({self.color!r})'


