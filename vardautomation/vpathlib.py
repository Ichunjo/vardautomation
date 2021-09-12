"""pathlib.Path inheritance"""

from __future__ import annotations
from typing import Any

__all__ = ['VPath']

from pathlib import Path


class VPath(Path):
    """Modified version of pathlib.Path"""
    # pylint: disable=no-member
    _flavour = type(Path())._flavour  # type: ignore

    def format(self, *args: Any, **kwargs: Any) -> VPath:
        """
        :return:        Formatted version of `vpath`,
                        using substitutions from args and kwargs.
                        The substitutions are identified by braces ('{' and '}')
        """
        return VPath(self.to_str().format(*args, **kwargs))

    def set_track(self, track_number: int, /) -> VPath:
        """
        Set the track number by replacing the substitution "{track_number}"
        by the track_number specified

        :param track_number:        Track number
        :return:                    Formatted VPath
        """
        return self.format(track_number=track_number)

    def to_str(self) -> str:
        """
        :return:        String representation of the path, suitable for
                        passing to system calls.
        """
        return str(self)
