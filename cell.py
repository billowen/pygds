from datetime import datetime
from misc import *
from exceptions import *
from polygon import *


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
        self.elments = []

    def read(stream):
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
                pos = stream.tell()
                stream.seek(pos - size)
                poly = Polygon()

