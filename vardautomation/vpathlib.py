"""pathlib.Path inheritance"""

from __future__ import annotations
from typing import Any

__all__ = ['VPath']

from pathlib import Path


class VPath(Path):
    """Vardë Path"""
    # pylint: disable=no-member
    _flavour = type(Path())._flavour  # type: ignore

    def format(self, *args: Any, **kwargs: Any) -> VPath:
        """
            vpath.format(*args, **kwargs) -> VPath

            Return a formatted version of `vpath`, using substitutions from args and kwargs.
            The substitutions are identified by braces ('{' and '}')
        """
        return VPath(self.to_str().format(*args, **kwargs))

    def set_track(self, track_number: int, /) -> VPath:
        return self.format(track_number=track_number)

    def to_str(self) -> str:
        """
            Return the string representation of the path, suitable for
            passing to system calls.
        """
        return str(self)
