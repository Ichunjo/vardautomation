from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

__author__ = "Ichunjo"
__maintainer__ = "Ichunjo"
__email__ = "ichunjo.le.terrible@gmail.com"
__status__ = "Development"

try:
    __version__ = _version("vardautomation")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"


def version() -> str:
    return __version__
