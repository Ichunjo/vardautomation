"""pathlib.Path inheritance"""

from __future__ import annotations

__all__ = ['VPath']

import os
import shutil
from pathlib import Path
from types import TracebackType
from typing import Any, Callable, Iterable, List, Optional, Protocol, Tuple, Type

from .status import Status
from .types import AnyPath, AbstractMutableSet


class _Flavour(Protocol):
    sep: str
    altsep: str


_ExcInfo = Tuple[Type[BaseException], BaseException, TracebackType]
_OptExcInfo = _ExcInfo | Tuple[None, None, None]  # type: ignore[operator]


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
        Stolen from pathlib3x

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

    def copy(self, target: AnyPath, *, follow_symlinks: bool = True) -> None:
        """
        Wraps shutil.copy. Stolen from pathlib3x.

        https://docs.python.org/3/library/shutil.html#shutil.copy

        :param target:              See Python official documentation
        :param follow_symlinks:     See Python official documentation
        """
        shutil.copy(self, target, follow_symlinks=follow_symlinks)

    def copy2(self, target: AnyPath, follow_symlinks: bool = True) -> None:
        """
        Wraps shutil.copy2. Stolen from pathlib3x.

        https://docs.python.org/3/library/shutil.html#shutil.copy2

        :param target:              See Python official documentation
        :param follow_symlinks:     See Python official documentation
        """
        shutil.copy2(self, target, follow_symlinks=follow_symlinks)

    def copyfile(self, target: VPath, follow_symlinks: bool = True) -> None:
        """
        Wraps shutil.copyfile. Stolen from pathlib3x.

        https://docs.python.org/3/library/shutil.html#shutil.copyfile

        :param target:              See Python official documentation
        :param follow_symlinks:     See Python official documentation
        """
        shutil.copyfile(self, target, follow_symlinks=follow_symlinks)

    def copymode(self, target: AnyPath, follow_symlinks: bool = True) -> None:
        """
        Wraps shutil.copymode. Stolen from pathlib3x.

        https://docs.python.org/3/library/shutil.html#shutil.copymode

        :param target:              See Python official documentation
        :param follow_symlinks:     See Python official documentation
        """
        shutil.copymode(self, target, follow_symlinks=follow_symlinks)

    def copystat(self, target: AnyPath, follow_symlinks: bool = True) -> None:
        """
        Wraps shutil.copystat. Stolen from pathlib3x.

        https://docs.python.org/3/library/shutil.html#shutil.copystat

        :param target:              See Python official documentation
        :param follow_symlinks:     See Python official documentation
        """
        shutil.copystat(self, target, follow_symlinks=follow_symlinks)

    def copytree(
        self, target: AnyPath, symlinks: bool = False,
        ignore: Optional[Callable[[AnyPath, List[str]], Iterable[str]]] = None,
        copy_function: Callable[[AnyPath, AnyPath], Any] = shutil.copy2,
        ignore_dangling_symlinks: bool = True, dirs_exist_ok: bool = False
    ) -> None:
        """
        Wraps shutil.copytree. Stolen from pathlib3x.

        https://docs.python.org/3/library/shutil.html#shutil.copytree

        :param target:                      See Python official documentation
        :param symlinks:                    See Python official documentation
        :param ignore:                      See Python official documentation
        :param copy_function:               See Python official documentation
        :param ignore_dangling_symlinks:    See Python official documentation
        :param dirs_exist_ok:               See Python official documentation
        """
        shutil.copytree(self, target, symlinks, ignore, copy_function, ignore_dangling_symlinks, dirs_exist_ok)

    def rmtree(self, ignore_errors: bool = False,
               onerror: Optional[Callable[[Callable[..., Any], str, _OptExcInfo], Any]] = None) -> None:
        """
        Wraps shutil.rmtree. Stolen from pathlib3x.

        https://docs.python.org/3/library/shutil.html#shutil.rmtree

        :param ignore_errors:           See Python official documentation
        :param onerror:                 See Python official documentation
        """
        shutil.rmtree(self, ignore_errors, onerror)

    def rm(self, ignore_errors: bool = False) -> None:
        """
        Wraps os.remove.

        :param ignore_errors:           Ignore errors emitted by os.remove
        """
        if ignore_errors:
            try:
                os.remove(self)
            except OSError:
                pass
        else:
            try:
                os.remove(self)
            except FileNotFoundError as file_err:
                Status.fail(
                    f'{self.__class__.__name__}: This file doesn\'t exist',
                    exception=FileNotFoundError, chain_err=file_err
                )
            except IsADirectoryError as dir_err:
                Status.fail(
                    f'{self.__class__.__name__}: {self} is a directory. Use ``rmtree`` instead.',
                    exception=IsADirectoryError, chain_err=dir_err
                )


class CleanupSet(AbstractMutableSet[VPath]):
    # pylint: disable=arguments-differ
    def clear(self, *, ignore_errors: bool = True) -> None:
        """
        Clear the set and delete files

        :param ignore_errors:       Ignore errors emitted by os.remove
        """
        for path in self:
            path.rm(ignore_errors)
        return super().clear()

    def add(self, value: AnyPath) -> None:
        """
        Add a generic path to this set and convert it to a VPath
        This has no effect if the path is already present

        :param value:       A path
        """
        return super().add(VPath(value))

    def discard(self, value: VPath) -> None:
        """
        Remove a VPath from this set if it is a member.
        If the VPath is not a member, do nothing

        :param value:       A VPath
        """
        return super().discard(value)

    def update(self, *s: Iterable[AnyPath]) -> None:
        """
        Update the set with the union of itself and others

        :param s:           Iterable of path
        """
        return super().update([VPath(p) for iterable in s for p in iterable])
