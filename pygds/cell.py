from datetime import datetime
from misc import *
from exceptions import *
from polygon import *
from aref import *
from sref import *
from path import *
from polygon import *
from text import *


class Cell(list):

    def __init__(self, name):

        self.name = name
        now = datetime.now()
        self.mod_year = now.year
        self.mod_month = now.month
        self.mod_day = now.day
        self.mod_hour = now.hour
        self.mod_minute = now.minute
        self.mod_second = now.second
        self.acc_year = now.year
        self.acc_month = now.month
        self.acc_day = now.day
        self.acc_hour = now.hour
        self.acc_minute = now.minute
        self.acc_second = now.second
        self.refer_by = []
        self.elements = []

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if (rec_type != RecordType['BGNSTR']):
            raise FormatError('Unexpected tag where BGNSTR is expected:', rec_type)
        elif size != 28:
            raise exceptions.IncorrectDataSize('The BGNSTR expects 28 bytes data')
        self.mod_year = read_short(stream)
        self.mod_month = read_short(stream)
        self.mod_day = read_short(stream)
        self.mod_hour = read_short(stream)
        self.mod_minute = read_short(stream)
        self.mod_second = read_short(stream)
        self.acc_year = read_short(stream)
        self.acc_month = read_short(stream)
        self.acc_day = read_short(stream)
        self.acc_hour = read_short(stream)
        self.acc_minute = read_short(stream)
        self.acc_second = read_short(stream)

        size, rec_type, _ = read_one_record(stream)
        while rec_type != RecordType['ENDSTR']:
            if rec_type == RecordType['STRNAME']:
                self.name = read_string(stream, size - 4)
            elif rec_type == RecordType['BOUNDARY']:
                stream.seek(-size, 1)
                poly = Polygon()
                poly.read(stream)
                self.elements.append(poly)
            elif rec_type == RecordType['PATH']:
                stream.seek(-size, 1)
                path = Path()
                path.read(stream)
                self.elements.append(path)
            elif rec_type == RecordType['TEXT']:
                stream.seek(-size, 1)
                text = Text()
                text.read(stream)
                self.elements.append(text)
            elif rec_type == RecordType['AREF']:
                stream.seek(-size, 1)
                aref = ARef()
                aref.read(stream)
                self.elements.append(aref)
            elif rec_type == RecordType['SREF']:
                stream.seek(-size, 1)
                sref = SRef()
                sref.read(stream)
                self.elements.append(sref)
            else:
                stream.seek(size - 4, 1)
            size, rec_type, _ = read_one_record(stream)

    def bbox(self):
        """ Get the bounding rect of a structure.

        Returns
            (llpoint, (width, height)): the first elment is a Point which indicates the low left vertex,
            and the second element is a tuple which indicates the width and height of bounding rect.

        Raises
            Exception: The structure has not been initialized."""
        if len(self.elements) == 0:
            raise Exception('There is no element in the cell.')

        (llx, lly), (width, height) = self.elements[0].bbox()
        urx = llx + width
        ury = lly + height
        for element in self.elements:
            (_llx, _lly), (_width, _height) = element.bbox()
            if _llx < llx:
                llx = _llx
            if _lly < lly:
                lly = _lly
            if _llx + _width > urx:
                urx = _llx + _width
            if _lly + _height > ury:
                ury = _lly + _height
        return (llx, lly), (urx - llx, ury - lly)


