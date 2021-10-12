"""Language module"""

from __future__ import annotations

__all__ = [
    'Lang',
    'FRENCH', 'ENGLISH', 'JAPANESE', 'UNDEFINED'
]


from pprint import pformat
from typing import Optional

from langcodes import Language

from .utils import recursive_dict


class Lang:
    """Basic language class"""

    name: str
    """Name of the language"""
    ietf: str
    """IETF BCP 47 language code"""
    iso639: str
    """ISO-639 language code"""

    def __init__(self, language: Language, *, iso639_variant: str = 'B') -> None:
        """
        :param language:        Language class of the package langcodes
        :param iso639_variant:  Optional variant to get the 'bibliographic' code instead, defaults to 'B'
        """
        self.name = language.autonym()
        self.ietf = str(language)
        self.iso639 = language.to_alpha3(variant=iso639_variant)

    def __str__(self) -> str:
        return pformat(recursive_dict(self), indent=4, width=200, sort_dicts=False)

    @classmethod
    def make(cls, ietf: Optional[str]) -> Lang:
        """
        Make a new Lang based on IETF

        :param ietf:            IETF BCP 47 language code
        :return:                A new Lang object
        """
        return cls(Language.make(ietf))


FRENCH = Lang.make('fr')
"""French Lang object"""

ENGLISH = Lang.make('en')
"""English Lang object"""

JAPANESE = Lang.make('ja')
"""Japanese Lang object"""

UNDEFINED = Lang.make(None)
"""Undefined Lang object"""
