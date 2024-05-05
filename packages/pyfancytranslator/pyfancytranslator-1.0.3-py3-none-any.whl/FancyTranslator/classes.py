import logging
import os
import re
from configparser import ConfigParser
from typing import Optional, Type, TypeVar, Union


class Parser:
    """
    Class which holds the data to be accessed by "Language" class
    WARNING: This class is not intended to be modified by users.
    """

    def __init__(self):
        self.data = {}

    def set(self, section: str, option: str, value: Optional[str]):
        section_dict = self.data.setdefault(section, {})
        section_dict[option] = value

    def get(self, section, option):
        return self.data.get(section, {}).get(option, None)


class Language:
    """
    Class which handles the translation for a language.
    Parameters:
        :param parser (Parser): Parser instance, aka the data holder
        :param code (str): Language code, aka the language file name
        :param name (str): Language name, read from the langauge file, section "Translation", key "name"
        :param logger (logging.Logger): The child logger of translator logger for this language
    """

    def __init__(self, translator: 'Translator', code: str):
        self.code = code

        cf = ConfigParser()
        cf.read(f"{translator.path}/{code}.ini")

        count = 0
        self.parser = Parser()
        for section in cf.sections():
            for option in cf.options(section):
                self.parser.set(section, option, cf.get(section, option))
                count += 1

        self.logger = translator.logger.getChild(code)
        self.name = self.parser.get("Translation", "name") or self.code
        self.logger.info(f"Language {self.code} has been loaded with {count} options in total")

    def read(self, section: str, key: str, default: str = None) -> Optional[str]:
        """
        Reads the value from the langauge file and returns it as a string.
        :param section: The section name to look for the translation from.
        :param key: The key to look for the translation from n the provided section.
        :param default: If translation not found, returns this value.
        :return: The value from the langauge file or default if no translation was found.

        Note: If translation not found, a warning will be logged as well.
        Note: This will only return the value and has no modifications built in.
        """
        if not isinstance(key, str) or not isinstance(section, str):
            return default

        text = self.parser.get(section, key)
        if text is None:
            self.logger.warning(f'Missing translation key "{key}" in section "{section}"')
            return default
        return text

    def translate(self, section: str, key: str, default: str = None, **kwargs: object) -> Optional[str]:
        """
        A more secure method than read, With built-in modifications known as placeholders.
        :param section: The section name to look for the translation from.
        :param key: The key to look for the translation from n the provided section.
        :param default: If translation not found, returns this value.
        :param kwargs: The placeholders to be used to replace in translation.
        :return: The value from the langauge file or default if no translation was found.

        To use placeholders, you should use the following syntax in the language file:
        ```ini
        [Target]
        trans1 = This is an example with a normal placeholder: %%value%%
        trans2 = This is an example with a nested placeholder: %%value.obj.name%%
        ```

        Placeholders supports normal as well as nested values.
        ```py
        class MyClass:
            def __init__(self, obj):
                self.obj = obj

        my_class = MyClass({"name": "Nested"})

        trans1 = translator.get('en').translate("Target", "trans1", value="My Value")
        # returns "This is an example with a normal placeholder: My Value"

        trans2 = translator.get('en').translate("Target", "trans2", value=my_class)
        # returns "This is an example with a nested placeholder: Nested"
        ```
        """
        text = self.read(section, key, default)
        if not isinstance(text, str):
            return text

        for placeholder in re.findall('%\\w+(\\.\\w+)*%', text):
            path = placeholder.split('.')
            obj: None | object = kwargs.get(path.pop(0), None)
            while obj is not None and len(path) > 0:
                if isinstance(obj, dict):
                    obj = obj.get(path.pop(0), None)
                else:
                    obj = getattr(obj, path.pop(0), None)

            text.replace(f'%{placeholder}%', str(obj) if obj is not None else f'None({placeholder})')

        return text


_TL = TypeVar('_TL', bound=Language)


class Translator:
    """
    Class holding all languages in the translation folder given.
    Parameters:
        :param path (str): The path to look for all translation files. Does not support nested folders.
        :param language_class (Type[Language]): The custom language class if needed.
        :param logger (Logger | str): Change the logger if needed.

    """
    def __init__(self, path: str = None, *, language_class: Type[_TL] = None, logger: Union[logging.Logger, str] = None):
        language_class = language_class or Language
        if not issubclass(language_class, Language):
            raise TypeError('"language_class" must be a subclass of Language')

        self.path = path or './'
        self.languages = {}
        self.logger = logging.getLogger('Translator') if logger is None else logging.getLogger(logger) if isinstance(logger, str) else logger

        for filename in os.listdir(self.path):
            if filename.endswith(".ini"):
                # noinspection PyBroadException
                try:
                    self.languages[filename[:-4]] = language_class(self, filename[:-4])
                except Exception:
                    self.logger.exception(f'Unable to load translation file: {filename}')

    def __getitem__(self, language: str) -> Optional[_TL]:
        return self.languages.get(language)

    def get(self, langauge: str) -> Optional[_TL]:
        return self.languages.get(langauge)
