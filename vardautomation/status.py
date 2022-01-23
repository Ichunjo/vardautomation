"""Logger module"""
import sys
import traceback
from typing import Any, List, NoReturn, Optional, Type

import colorama
import pkg_resources

from ._logging import logger

colorama.init()


class FileError(OSError):
    ...


class VSFormatError(ValueError):
    ...


class VSSubsamplingError(VSFormatError):
    ...


class VSColourRangeError(ValueError):
    ...


class Colours:
    """Colour constants"""
    FAIL_DIM: str = colorama.Back.RED + colorama.Fore.BLACK + colorama.Style.NORMAL
    FAIL_BRIGHT: str = colorama.Back.RED + colorama.Fore.WHITE + colorama.Style.NORMAL
    WARN: str = colorama.Back.YELLOW + colorama.Fore.BLACK + colorama.Style.NORMAL
    INFO: str = colorama.Back.BLUE + colorama.Fore.WHITE + colorama.Style.BRIGHT
    RESET: str = colorama.Style.RESET_ALL
    FAILS: List[str] = [FAIL_DIM, FAIL_BRIGHT]


class Status:
    __slots__ = ()

    @staticmethod
    def fail(string: str, /, *, exception: Type[BaseException] = Exception, chain_err: Optional[BaseException] = None) -> NoReturn:
        logger.warning('Using Status is deprecated; please use "logger" instead')
        curr_split: List[str] = []

        # All that stuff is just for alternating colours lmao
        if chain_err:
            class _Exception(BaseException):
                __cause__ = chain_err

            curr = _Exception()

            for p in traceback.format_exception(None, curr, None)[:-1]:
                curr_split.extend(p.splitlines(keepends=True))

        for p in traceback.format_stack()[:-2]:
            curr_split.extend(p.splitlines(keepends=True))

        curr_split.append(f'{exception.__name__}: {string}')

        curr_split = [Colours.FAILS[i % 2] + line + Colours.RESET for i, line in enumerate(curr_split[::-1])][::-1]
        sys.exit(''.join(curr_split) + Colours.RESET)

    @staticmethod
    def warn(string: str, /) -> None:
        logger.warning('Using Status is deprecated; please use "logger" instead')
        print(f'{Colours.WARN}{string}{Colours.RESET}')

    @staticmethod
    def info(string: str, /, **kwargs: Any) -> None:
        logger.warning('Using Status is deprecated; please use "logger" instead')
        print(f'{Colours.INFO}{string}{Colours.RESET}', **kwargs)

    @staticmethod
    def logo() -> None:
        logger.warning('Using Status is deprecated; please use "logger" instead')
        with open(pkg_resources.resource_filename('vardautomation', 'logo.txt'), 'r', encoding='utf-8') as logo:
            print(''.join(Colours.INFO + line + Colours.RESET for line in logo.readlines()), '\n')
