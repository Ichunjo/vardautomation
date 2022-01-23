"""Logger module"""

from typing import Any, List, NoReturn, Optional, Type

import colorama

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
        with logger.catch_ctx():
            raise exception(string) from chain_err

    @staticmethod
    def warn(string: str, /) -> None:
        logger.warning('Using Status is deprecated; please use "logger" instead')
        logger.warning(string)

    @staticmethod
    def info(string: str, /, **kwargs: Any) -> None:
        logger.warning('Using Status is deprecated; please use "logger" instead')
        logger.info(string)

    @staticmethod
    def logo() -> None:
        logger.warning('Using Status is deprecated; please use "logger" instead')
        logger.logo()
