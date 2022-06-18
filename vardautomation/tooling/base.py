
__all__ = ['BasicTool']

import subprocess
from typing import Any, Dict, List, Optional

from .._logging import logger
from ..config import FileInfo
from ..types import AnyPath
from ..utils import copy_docstring_from
from .abstract import Tool


class BasicTool(Tool):
    """BasicTool interface."""

    file: Optional[FileInfo]
    """FileInfo object."""

    def __init__(self, binary: AnyPath, settings: AnyPath | List[str] | Dict[str, Any], /,
                 file: Optional[FileInfo] = None, check_binary: bool = True) -> None:
        """
        Helper allowing the use of CLI programs for basic tasks like video or audio track extraction.

        :param binary:          See :py:attr:`Tool.binary`
        :param settings:        See :py:attr:`Tool.settings`
        :param file:            Not used in BasicTool implementation, defaults to None
        :param check_binary:        Check binary's availability.
        """
        self.file = file
        super().__init__(binary, settings, check_binary=check_binary)

    def run(self) -> None:
        self._update_settings()
        self._do_tooling()

    @copy_docstring_from(Tool.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """No variable are replaced there."""
        return {}

    def _do_tooling(self) -> None:
        logger.info(f'{self.binary.to_str()} command: ' + ' '.join(self.params))
        with logger.catch_ctx():
            subprocess.run(self.params, check=True, text=True, encoding='utf-8')
