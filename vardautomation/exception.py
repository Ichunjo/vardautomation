"""Logger module"""


class FileError(OSError):
    ...


class VSFormatError(ValueError):
    ...


class VSSubsamplingError(VSFormatError):
    ...


class VSColourRangeError(ValueError):
    ...
