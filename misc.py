import exceptions
import struct


RecordType = {
    'HEADER': 0x00,
    'BGNLIB': 0x01,
    'LIBNAME': 0x02,
    'UNITS': 0x03,
    'ENDLIB': 0x04,
    'BGNSTR': 0x05,
    'STRNAME': 0x06,
    'ENDSTR': 0x07,
    'BOUNDARY': 0x08,
    'PATH': 0x09,
    'SREF': 0x0a,
    'AREF': 0x0b,
    'TEXT': 0x0c,
    'LAYER': 0x0d,
    'DATATYPE': 0x0e,
    'WIDTH': 0x0f,
    'XY': 0x10,
    'ENDEL': 0x11,
    'SNAME': 0x12,
    'COLROW': 0x13,

    'TEXTTYPE': 0x16,
    'PRESENTATION': 0x17,

    'STRING': 0x19,
    'STRANS': 0x1a,
    'MAG': 0x1b,
    'ANGLE': 0x1c,

    'PATHTYPE': 0x21,

    'EFLAGS': 0x26,
}


class Point:

    def __init__(self, x = 0, y = 0):

        self.x = x
        self.y = y


def read_one_record(stream):
    '''Read a record header from gds stream.

    Args:
        stream: The io stream represent the gds data.

    Returns:
        A tuple which contains the information of record length,
        record type and data type. For example (size, rec_type, dt)

    Raises:
        exceptions.EndOfFileError: Meet the end of file unexpectly.
    '''
    header = stream.read(4)
    if not header or len(header) != 4:
        raise exceptions.EndOfFileError

    return struct.unpack('>Hcc', header)


def read_short(stream):
    '''Read a short from gds stream.

    Args:
        stream: The io stream represent the gds data.

    Returns:
        An int number.

    Raises:
        exceptions.EndOfFileError: Meet the end of file unexpectly.
    '''
    bin_data = stream.read(2)
    if not bin_data or len(bin_data) != 2:
        raise exceptions.EndOfFileError

    data = struct.unpack('>h', bin_data)
    return data


def read_integer(stream):
    '''Read a integer from gds stream.

    Args:
        stream: The io stream represent the gds data.

    Returns:
        An int number.

    Raises:
        exceptions.EndOfFileError: Meet the end of file unexpectly.
    '''
    bin_data = stream.read(4)
    if not bin_data or len(bin_data) != 4:
        raise exceptions.EndOfFileError
    data = struct.unpack('>i', bin_data)
    return data


def read_string(stream, size):
    '''Read a string from gds stream.

    Args:
        stream: The io stream represent the gds data.
        size: The lenght of string.

    Returns:
        A string.

    Raises:
        exceptions.EndOfFileError: Meet the end of file unexpectly.
    '''
    bin_data = stream.read(size)
    if not bin_data or len(bin_data) != size:
        raise exceptions.EndOfFileError
    return struct.unpack('>{0}s'.format(size), bin_data)


def read_bitarray(stream):
    '''Read a bit array from gds stream.

    Args:
        stream: The io stream represent the gds data.

    Returns:
        An int.

    Raises:
        exceptions.EndOfFileError: Meet the end of file unexpectly.
    '''
    bin_data = stream.read(2)
    if not bin_data or len(bin_data) != 2:
        raise exceptions.EndOfFileError

    data = struct.unpack('>H', bin_data)
    return data


def read_float(stream):
    '''Read a float from gds stream.

    Args:
        stream: The io stream represent the gds data.

    Returns:
        A float.

    Raises:
        exceptions.EndOfFileError: Meet the end of file unexpectly.
    '''
    bin_data = stream.read(8)
    if not bin_data or len(bin_data) != 8:
        raise exceptions.EndOfFileError
    short1, short2, long3 = struct.unpack('>HHL', bin_data)
    exponent = (short1 & 0x7f00) // 256
    mantissa = (((short1 & 0x00ff) * 65536 + short2) * 4294967296 + long3) / 72057594037927936.0
    return (-1 if (short1 & 0x8000) else 1) * mantissa * 16 ** (exponent - 64)

