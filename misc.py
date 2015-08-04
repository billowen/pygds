import exceptions
import struct


RecordType = {
    'HEADER':   b'\x00',
    'BGNLIB':   b'\x01',
    'LIBNAME':  b'\x02',
    'UNITS':    b'\x03',
    'ENDLIB':   b'\x04',
    'BGNSTR':   b'\x05',
    'STRNAME':  b'\x06',
    'ENDSTR':   b'\x07',
    'BOUNDARY': b'\x08',
    'PATH':     b'\x09',
    'SREF':     b'\x0a',
    'AREF':     b'\x0b',
    'TEXT':     b'\x0c',
    'LAYER':    b'\x0d',
    'DATATYPE': b'\x0e',
    'WIDTH':    b'\x0f',
    'XY':       b'\x10',
    'ENDEL':    b'\x11',
    'SNAME':    b'\x12',
    'COLROW':   b'\x13',

    'TEXTTYPE': b'\x16',
    'PRESENTATION': b'\x17',

    'STRING':   b'\x19',
    'STRANS':   b'\x1a',
    'MAG':      b'\x1b',
    'ANGLE':    b'\x1c',

    'PATHTYPE': b'\x21',
    'EFLAGS':   b'\x26',
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
    tmp = struct.unpack('>{0}s'.format(size), bin_data)
    return tmp[0].decode()


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

