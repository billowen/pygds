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

    def read(self, stream):
        self.clear()
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['BGNSTR']:
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
                self.append(poly)
            elif rec_type == RecordType['PATH']:
                stream.seek(-size, 1)
                path = Path()
                path.read(stream)
                self.append(path)
            elif rec_type == RecordType['TEXT']:
                stream.seek(-size, 1)
                text = Text()
                text.read(stream)
                self.append(text)
            elif rec_type == RecordType['AREF']:
                stream.seek(-size, 1)
                aref = ARef()
                aref.read(stream)
                self.append(aref)
            elif rec_type == RecordType['SREF']:
                stream.seek(-size, 1)
                sref = SRef()
                sref.read(stream)
                self.append(sref)
            else:
                stream.seek(size - 4, 1)
            size, rec_type, _ = read_one_record(stream)

    def bbox(self):
        """ Get the bounding rect of a structure.

        Returns
            bbox: the BBox which indicates the bbox of current gds element or none if failed to calculate the bbox.
        """
        if len(self) == 0:
            return None

        llx = GDS_MAX_INT
        lly = GDS_MAX_INT
        urx = GDS_MIN_INT
        ury = GDS_MIN_INT
        have_valid_element = False
        for element in self:
            if isinstance(element, Text):
                continue
            _bbox = element.bbox()
            if _bbox is None:
                continue
            have_valid_element = True
            if _bbox.x < llx:
                llx = _bbox.x
            if _bbox.y < lly:
                lly = _bbox.y
            if _bbox.x + _bbox.width > urx:
                urx = _bbox.x + _bbox.width
            if _bbox.y + _bbox.height > ury:
                ury = _bbox.y + _bbox.height
        if have_valid_element is False:
            return None
        return BBox(llx, lly, urx - llx, ury - lly)


