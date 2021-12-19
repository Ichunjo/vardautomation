
__all__ = ['BasicTool']

import subprocess
from typing import Any, Dict, List, Optional, Union

from ..config import FileInfo
from ..status import Status
from ..types import AnyPath
from ..utils import copy_docstring_from
from .abstract import Tool


class BasicTool(Tool):
    """BasicTool interface."""

    file: Optional[FileInfo]
    """FileInfo object."""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 file: Optional[FileInfo] = None) -> None:
        """
        Helper allowing the use of CLI programs for basic tasks like video or audio track extraction.

        :param binary:          See :py:attr:`Tool.binary`
        :param settings:        See :py:attr:`Tool.settings`
        :param file:            Not used in BasicTool implementation, defaults to None
        """
        self.file = file
        super().__init__(binary, settings)

    def run(self) -> None:
        self._update_settings()
        self._do_tooling()

    @copy_docstring_from(Tool.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """No variable are replaced there."""
        return {}

    def _do_tooling(self) -> None:
        Status.info(f'{self.binary.to_str()} command: ' + ' '.join(self.params))
        subprocess.run(self.params, check=True, text=True, encoding='utf-8')
