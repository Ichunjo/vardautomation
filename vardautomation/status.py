"""Logger module"""
from typing import NoReturn, Optional, Type

import colorama

colorama.init()


class Colours:
    FAIL: str = f'{colorama.Back.RED}{colorama.Fore.BLACK}'
    WARN: str = f'{colorama.Back.YELLOW}{colorama.Fore.BLACK}'
    INFO: str = f'{colorama.Back.BLUE}{colorama.Fore.WHITE}{colorama.Style.BRIGHT}'
    RESET: str = colorama.Style.RESET_ALL


class Status:
    @staticmethod
    def fail(string: str, /, *, exception: Type[Exception] = Exception, chain_err: Optional[Exception] = None) -> NoReturn:
        raise exception(f'{Colours.FAIL}{string}{Colours.RESET}') from chain_err

    @staticmethod
    def warn(string: str, /, raise_error: bool = False, *,
             exception: Optional[Type[Exception]] = Exception, chain_err: Optional[Exception] = None) -> None:
        if not raise_error:
            print(f'{Colours.WARN}{string}{Colours.RESET}')
        else:
            if exception:
                raise exception(f'{Colours.WARN}{string}{Colours.RESET}') from chain_err

    @staticmethod
    def info(string: str, /, raise_error: bool = False, *,
             exception: Optional[Type[Exception]] = Exception, chain_err: Optional[Exception] = None) -> None:
        if not raise_error:
            print(f'{Colours.INFO}{string}{Colours.RESET}')
        else:
            if exception:
                raise exception(f'{Colours.INFO}{string}{Colours.RESET}') from chain_err
