from __future__ import annotations

from typing import Optional

from langcodes import Language


class Lang:
    name: str
    ietf: str
    iso639: str
    def __init__(self, language: Language, *, iso639_variant: str = ...) -> None: ...
    @classmethod
    def make(cls, ietf: Optional[str]) -> Lang: ...


FRENCH: Lang
ENGLISH: Lang
JAPANESE: Lang
UNDEFINED: Lang
