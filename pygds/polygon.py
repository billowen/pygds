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
        """ Get the bounding rect of polygon.

        Returns
            bbox: the BBox which indicates the bbox of current gds element or none if failed to calculate the bbox.
        """
        if self.pts is None:
            raise Exception("The polygon has not been initialized correctly.")
        llx = self.pts[0].x
        lly = self.pts[0].y
        urx = self.pts[0].x
        ury = self.pts[0].y
        for pp in self.pts:
            if pp.x < llx:
                llx = pp.x
            if pp.x > urx:
                urx = pp.x
            if pp.y < lly:
                lly = pp.y
            if pp.y > ury:
                ury = pp.y

        return BBox(llx, lly, urx - llx, ury - lly)


class Rect(Polygon):
    def __init__(self):
        super().__init__()

    def set(self, x, y, width, height):
        vertex = list()
        vertex.append(Point(x, y))
        vertex.append(Point(x + width, y))
        vertex.append(Point(x + width, y + height))
        vertex.append(Point(x, y + height))
        vertex.append(Point(x, y))
        Polygon.pts.fset(self, vertex)

    @property
    def pts(self):
        return Polygon.pts.fget(self)

    @pts.setter
    def pts(self, pts):
        if len(pts) != 5:
            raise Exception('Invalid input of Rect: the number of points used to initialize Rect should be 5.')
        elif pts[0].x != pts[-1].x or pts[0].y != pts[-1].y:
            raise Exception('Invalid input of Rect: '
                            'The XY expects the same coordinates of the first vertex and the last vertex.')
        Polygon.pts.fget(self, pts)

