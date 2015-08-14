from elementbase import ElementBase
from misc import *
import struct
from exceptions import *


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
        elif pts[0].x != pts[-1].x or pts[0].y != pts[-1].y:
            raise Exception('The XY expects the same coordinates of the first vertex and the last vertex.') 
        self._pts = pts

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['BOUNDARY']:
            raise FormatError('Unexpected tag where BOUNDARY is expected:', rec_type)

        size, rec_type, _ = read_one_record(stream)
        while rec_type != RecordType['ENDEL']:
            if rec_type == RecordType['EFLAGS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['LAYER']:
                self.layer = read_short(stream)
            elif rec_type == RecordType['DATATYPE']:
                self.data_type = read_short(stream)
            elif rec_type == RecordType['XY']:
                if (size - 4) % 8 != 0:
                    raise IncorrectDataSize('XY')
                p_num = int((size - 4) / 8)
                p_list = []
                for i in range(p_num):
                    x = read_integer(stream)
                    y = read_integer(stream)
                    p_list.append(Point(x, y))
                self.pts = p_list
            else:
                stream.seek(size - 4, 1)

            size, rec_type, _ = read_one_record(stream)

    def bbox(self):
        if pts == None:
            raise Exception("The polygon has not been initialized correctly.")
        llx = pts[0].x
        lly = pts[0].y
        urx = pts[0].x
        ury = pts[0].y
        for pp in pts:
            if pp.x < llx:
                llx = pp.x
            if pp.x > urx:
                urx = pp.x
            if pp.y < lly:
                lly = pp.y
            if pp.y > ury:
                ury = pp.y

        return (Point(llx, lly), Point(urx, ury))


if __name__ == "__main__":
    s = struct.unpack('>3s', b'\x61\x62\x63')
    print(s)
    ss = s[0].decode()
    print(ss)