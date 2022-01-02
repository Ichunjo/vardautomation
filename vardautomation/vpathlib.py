"""pathlib.Path inheritance"""

from __future__ import annotations

__all__ = ['VPath']

from pathlib import Path
from typing import Any, Protocol


class _Flavour(Protocol):
    sep: str
    altsep: str


class VPath(Path):
    """Modified version of pathlib.Path"""
    # pylint: disable=no-member
    _flavour: _Flavour = type(Path())._flavour  # type: ignore

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

    def append_stem(self, stem: str) -> VPath:
        """
        Append ``stem`` at the end of the VPath stem

        :param stem:                Stem to add
        :return:                    New VPath with the stem appended
        """
        return self.with_stem(self.stem + stem)

    def append_suffix(self, suffix: str) -> VPath:
        """
        Append ``stem`` at the end of the VPath suffix.
        Stoled from pathlib3x

        :param suffix:              Suffix to add. It has to start with '.'
        :return:                    New VPath with the file suffix appended
        """
        f = self._flavour
        if f.sep in suffix or f.altsep and f.altsep in suffix:
            raise ValueError(f'Invalid suffix {suffix}')
        if suffix and not suffix.startswith('.') or suffix == '.':
            raise ValueError(f'Invalid suffix {suffix}')
        name = self.name
        if not name:
            raise ValueError(f'{self} has an empty name')
        name = name + suffix
        return self._from_parsed_parts(self._drv, self._root, self._parts[:-1] + [name])  # type: ignore
