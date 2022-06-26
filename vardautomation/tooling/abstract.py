

__all__ = ['Tool']

import re
import subprocess
from abc import ABC, abstractmethod
from typing import Any, Dict, List, NoReturn

from .._logging import logger
from ..types import AnyPath
from ..vpathlib import VPath


class Tool(ABC):
    """
    Abstract Tool interface.\n
    Most of the tools inherit from it.
    """

    binary: VPath
    """Binary path"""

    params: List[str]
    """Settings normalised and parsed"""

    def __init__(self, binary: AnyPath, settings: AnyPath | List[str] | Dict[str, Any], *, check_binary: bool = True) -> None:
        """
        ::

            # This
            >>> cat settings
            -o {clip_output:s} - --y4m --preset slower --crf 51

            # is equivalent to this:
            settings: List[str] = ['-o', '{clip_output:s}', '-', '--y4m', '--preset', 'slower', '--crf', '51']

            # and is equivalent to this:
            settings: Dict[str, Any] = {
                '-o': '{clip_output:s}',
                '-': None,
                '--y4m': None,
                '--preset': 'slower',
                '--crf': 51
            }

        :param binary:              Path to your binary file.
        :param settings:            Path to your settings file or list of string or a dict containing your settings
                                    Special variable names can be specified and are replaced at runtime.
                                    Supported variable names are defined in :py:func:`set_variable` docstring.
        :param check_binary:        Check binary's availability.
        """
        self.binary = VPath(binary)

        if isinstance(settings, dict):
            for k, v in settings.items():
                self.params.extend([k] + ([str(v)] if v else []))
        elif isinstance(settings, list):
            self.params = settings.copy()
        else:
            try:
                with open(settings, 'r', encoding='utf-8') as sttgs:
                    params_re = re.split(r'[\n\s]\s*', sttgs.read())
            except FileNotFoundError as file_err:
                logger.critical(f'{self.__class__.__name__}: settings file not found', file_err)
            self.params = [p for p in params_re if isinstance(p, str)]

        if check_binary:
            self._check_binary()

        self.params = [x for x in self.params if x]
        self.params.insert(0, self.binary.to_str())

        super().__init__()

    @abstractmethod
    def run(self) -> None | NoReturn:
        """Tooling chain"""

    @abstractmethod
    def set_variable(self) -> Dict[str, Any]:
        """
        Set variables in the settings\n
        """

    @property
    def _quiet(self) -> bool:
        return logger.level >= logger.info.no

    @logger.catch
    def _update_settings(self) -> None:
        for i, p in enumerate(self.params):
            if not re.findall(r'(?<=(?<!\{)\{)[^{}]*(?=\}(?!\}))', p):
                continue
            p = p.format(**self.set_variable())
            self.params[i] = p

    def _check_binary(self) -> None:
        try:
            subprocess.call(self.binary.to_str(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except FileNotFoundError as file_not_found:
            logger.critical(f'{self.__class__.__name__}: "{self.binary.to_str()}" was not found!', file_not_found)
