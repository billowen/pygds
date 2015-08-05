from elementbase import ElementBase
from misc import *
import struct


class Polygon(ElementBase):

    def __init__(self):
        super().__init__('BOUNDARY')
        self.eflags = 0
        self.layer = -1
        self.data_type = -1
        self._pts = None

    @property
    def pts(self):
        return self._pts

    @pts.setter
    def pts(self, pts):
        if len(pts) < 4:
            raise Exception('The XY expects more then 4 pairs in BOUNDARY')
        elif pts[0] != pts[-1]:
            raise Exception('The XY expects the same coordinates of the first vertex and the last vertex.') 
        self._pts = pts

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['BOUNDARY']:
            raise exceptions.FormatError('Unexpected tag where BOUNDARY is expected:', rec_type)

        size, rec_type, _ = read_one_record(stream)
        while rec_type != RecordType['ENDEL']:
            if rec_type == RecordType['EFLAGS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['LAYER']:
                self.layer = read_short(stream)
            elif rec_type == RecrodType['DATATYPE']:
                self.data_type = read_short(stream)
            elif rec_type == RecrodType['XY']:
                if (size - 4) % 8 != 0:
                    raise exceptions.IncorrectDataSize('XY')
                p_num = (size - 4) / 8
                p_list = []
                for i in range(p_num):
                    x = read_integer(stream)
                    y = read_integer(stream)
                    p_list.append(Point(x, y))
                self.pts = p_list
            else:
                stream.seek(size - 4, 1)

            size, rec_type, _ = read_one_record(stream)



if __name__ == "__main__":
    s = struct.unpack('>3s', b'\x61\x62\x63')
    print(s)
    ss = s[0].decode()
    print(ss)