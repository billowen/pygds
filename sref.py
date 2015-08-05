from misc import *
import exceptions
from elementbase import ElementBase

class SRef(ElementBase):

    def __init__(self):

        super().__init__('SREF')
        self.eflags = 0
        self.strans = 0
        self.sname = ""
        self.angle = 0.0
        self.mag = 1.0
        self.pt = None
        slef.refer_to = None

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['SREF']:
            raise exceptions.FormatError('Unexpected tag where SREF is expected:', rec_type)

        size, rec_type, _ = read_one_record(stream)
        while rec_type != RecordType['ENDEL']:
            if rec_type == RecordType['EFLAGS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['STRANS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['SNAME']:
                self.sname = read_string(stream, size - 4)
            elif rec_type == RecordType['ANGLE']:
                self.angle = read_float(stream)
            elif rec_type == RecordType['MAG']:
                self.mag = read_float(stream)
            elif rec_type == RecoreType['XY']:
                x = read_integer(stream)
                y = read_integer(stream)
                self.pts = Point(x, y)
            else:
                stream.seek(size - 4, 1)
            size, rec_type, _ = read_one_record(stream)