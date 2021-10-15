

__all__ = [
    'Tool'
]

import re
import subprocess
import sys
import traceback
from abc import ABC, abstractmethod
from typing import Any, Dict, List, NoReturn, Union

from ..status import Status
from ..types import AnyPath
from ..vpathlib import VPath


class Tool(ABC):
    """
    Abstract Tool interface.\n
    Most of the tools inherit from it.
    """

    binary: VPath
    """Binary path"""

    settings: Union[AnyPath, List[str], Dict[str, Any]]
    """
    Path to your settings file or list of string or a dict containing your settings.

    .. code-block:: python

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
    """

    params: List[str]
    """Settings normalised and parsed"""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]]) -> None:
        """
        :param binary:              Path to your binary file.
        :param settings:            Path to your settings file or list of string or a dict containing your settings.
                                    See :py:attr:`Tool.settings`
        """
        self.binary = VPath(binary)
        self.settings = settings
        super().__init__()

    @abstractmethod
    def run(self) -> Union[None, NoReturn]:
        """Tooling chain"""

    @abstractmethod
    def set_variable(self) -> Dict[str, Any]:
        """Set variables in the settings"""

    def _get_settings(self) -> None:
        self.params = []
        if isinstance(self.settings, dict):
            for k, v in self.settings.items():
                self.params += [k] + ([str(v)] if v else [])
        elif isinstance(self.settings, list):
            self.params += self.settings
        else:
            try:
                with open(self.settings, 'r', encoding='utf-8') as sttgs:
                    params_re = re.split(r'[\n\s]\s*', sttgs.read())
            except FileNotFoundError as file_err:
                Status.fail(
                    f'{self.__class__.__name__}: settings file not found',
                    exception=FileNotFoundError, chain_err=file_err
                )
            self.params += [p for p in params_re if isinstance(p, str)]

        self._check_binary()

        params_parsed: List[str] = []
        for p in self.params:
            # pylint: disable=W0702
            try:
                p = p.format(**self.set_variable())
            except AttributeError:
                Status.warn(f'{self.__class__.__name__}: param {p} is not a str object; trying to convert to str...')
                p = str(p).format(**self.set_variable())
            except:  # noqa: E722
                excp_type, excp_val, trback = sys.exc_info()
                Status.fail(
                    f'{self.__class__.__name__}: Unexpected exception from the following traceback:\n'
                    + ''.join(traceback.format_tb(trback))
                    + (excp_type.__name__ if excp_type else Exception.__name__) + ': '
                    + str(excp_val), exception=Exception, chain_err=excp_val
                )
            params_parsed.append(p)
        self.params.clear()
        self.params = [self.binary.to_str()] + params_parsed

    def _check_binary(self) -> None:
        try:
            subprocess.call(self.binary.to_str(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except FileNotFoundError as file_not_found:
            Status.fail(
                f'{self.__class__.__name__}: "{self.binary.to_str()}" was not found!',
                exception=FileNotFoundError, chain_err=file_not_found
            )
