"""Collection of classes and helper functions to automate encoding"""
# flake8: noqa
from ._deprecated import *
from ._logging import *
from ._metadata import __author__, __version__, version  # type: ignore
from .automation import *
from .binary_path import *
from .chapterisation import *
from .comp import *
from .config import *
from .language import *
from .render import *
from .tooling import *
from .types import *
from .vpathlib import *

# for wildcard imports
_mods = [
    'automation', 'binary_path', 'chapterisation', 'comp', 'config', 'language',
    'render', 'tooling', 'types', 'vpathlib'
]

__all__ = []
for _pkg in _mods:
    __all__ += __import__(__name__ + '.' + _pkg, fromlist=_mods).__all__  # type: ignore
