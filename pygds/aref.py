from elementbase import ElementBase
from misc import *
import exceptions


class ARef(ElementBase):

    def __init__(self):

        super().__init__('AREF')
        self.eflags = 0
        self.strans = 0
        self.row = 0
        self.col = 0
        self.sname = ''
        self.angle = 0.0
        self.mag = 1.0
        self._pts = None
        self.refer_to = None

    @property
    def pts(self):
        return self._pts

    @pts.setter
    def pts(self, pts):
        if len(pts) != 3:
            raise exception('the xy expects 3 pairs for aref.') 
        self._pts = pts

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['AREF']:
            raise exceptions.FormatError('Unexpected tag where AREF is expected:', rec_type)

        size, rec_type, _ = read_one_record(stream)
        while rec_type != RecordType['ENDEL']:
            if rec_type == RecordType['EFLAGS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['STRANS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['COLROW']:
                self.col = read_short(stream)
                self.row = read_short(stream)
            elif rec_type == RecordType['SNAME']:
                self.sname = read_string(stream, size - 4)
            elif rec_type == RecordType['ANGLE']:
                self.angle = read_float(stream)
            elif rec_type == RecordType['MAG']:
                self.mag = read_float(stream)
            elif rec_type == RecordType['XY']:
                p_list = []
                for i in range(3):
                    x = read_integer(stream)
                    y = read_integer(stream)
                    p_list.append(Point(x, y))
                self.pts = p_list
            else:
                stream.seek(size - 4, 1)
            size, rec_type, _ = read_one_record(stream)
