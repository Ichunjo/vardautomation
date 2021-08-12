from langcodes import Language
from typing import Any, Optional

class Lang:
    name: str
    ietf: str
    iso639: str
    def __init__(self, language: Language, *, iso639_variant: str = ...) -> None: ...
    @classmethod
    def make(cls, ietf: Optional[str]) -> Lang: ...

FRENCH: Any
ENGLISH: Any
JAPANESE: Any
UNDEFINED: Any
