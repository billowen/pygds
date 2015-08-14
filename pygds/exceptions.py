class FormatError(Exception):

    """Base class for all GDSII exceptions."""


class EndOfFileError(FormatError):

    """Raised on unexpected end of file."""


class IncorrectDataSize(FormatError):

    """Raised if data size is incorrect."""


class UnsupportedTagType(FormatError):

    """Raised on unsupported tag type."""


class MissingRecord(FormatError):

    """Raised when required record is not found."""


class DataSizeError(FormatError):

    """Raised when data size is incorrect for a given record."""
