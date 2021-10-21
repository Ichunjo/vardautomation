"""Collection of classes and helper functions to automate encoding"""
# flake8: noqa
from .automation import *
from .binary_path import *
from .chapterisation import *
from .comp import *
from .config import *
from .language import *
from .tooling import *
from .types import *
from .vpathlib import *

# for wildcard imports
_mods = ['automation', 'binary_path', 'chapterisation', 'comp', 'config', 'language', 'tooling', 'types', 'vpathlib']

__all__ = []
for _pkg in _mods:
    __all__ += __import__(__name__ + '.' + _pkg, fromlist=_mods).__all__  # type: ignore

__author__ = __maintainer__ = 'Ichunjo'
__email__ = 'ichunjo.le.terrible@gmail.com'
__version__ = '0.5.0'
