"""
This is a module for working with languages.

Functions:
- lang(): Returns the current language code.
- define_lang(language: str): Sets the current language code to the specified code.
- all_langs(): Returns a list of all valid language codes.

Constants:
- LANGUAGES: A list of all valid language codes.

Example usage:
    >>> import language

    >>> print(language.lang())  # prints 'en'
    >>> language.define_lang('es')
    >>> print(language.lang())  # prints 'es'
    >>> print(language.all_langs())  # prints ['en', 'es']
"""


class LanguageError(ValueError):
    pass


def singleton(lang):
    def wrapper(cls):
        instances = {}

        def getinstance():
            if lang not in instances:
                instances[lang] = cls()
            return instances[lang]

        return getinstance

    return wrapper

@singleton('en')
class Language:
    _language = 'en'

    LANGUAGES = [
        ENG := 'en',
        ESP := 'es',
    ]

    def lang(self) -> str:
        return self._language

    def define_lang(self, language: str) -> None:
        if language not in self.LANGUAGES:
            raise LanguageError(f'Invalid language: {language!r}')
        self._language = language

    def all_langs(self) -> str:
        return self.LANGUAGES

    def print_langs(self) -> None:
        for lang in self.LANGUAGES:
            print(lang)

    def __contains__(self, language: str) -> bool:
        return language in self.LANGUAGES

    def __str__(self) -> str:
        return self._language

    def __repr__(self) -> str:
        return f'Language({self._language!r})'

    def __getitem__(self, language: str) -> str:
        if language not in self.LANGUAGES:
            raise LanguageError(f'Invalid language: {language!r}')
        return language


_language = Language()


def lang() -> str:
    return str(_language)


def define_lang(language: str) -> None:
    _language.define_lang(language)


def all_langs() -> str:
    return _language.all_langs()


def print_langs() -> None:
    _language.print_langs()
