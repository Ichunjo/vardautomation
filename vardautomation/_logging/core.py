from __future__ import annotations

__all__: list[str] = [
    "handler",
    "logger",
    "logo",
    "setup_logging",
    "show_logo",
]

import importlib.resources as impr
import logging

from rich.console import Console
from rich.logging import RichHandler
from rich.text import Text

handler = RichHandler(
    console=Console(stderr=True),
    omit_repeated_times=False,
    show_time=True,
    rich_tracebacks=True,
    log_time_format=lambda dt: Text(f"[{dt.strftime('%H:%M:%S')}.{dt.microsecond // 1000:03d}]"),
)
handler.setFormatter(logging.Formatter("{name}: {message}", style="{"))

logger = logging.getLogger("vardautomation")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False


def setup_logging(level: int | str = logging.INFO) -> None:
    """Configure vardautomation logging level."""
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(level)
    handler.setLevel(level)


def show_logo() -> None:
    """Display vardautomation logo in console."""
    lines = impr.files("vardautomation").joinpath("logo.txt").read_text(encoding="utf-8")
    logger.debug("Displaying that based vardautomation logo")
    Console(stderr=True).print(f"[blue][bold]\n{lines}\n[/]")


logo = show_logo
