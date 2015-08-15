from elementbase import ElementBase
from misc import *
import exceptions

class Path(ElementBase):

    def __init__(self):
        super().__init__('PATH')

        self.eflags = 0
        self.layer = -1
        self.data_type = -1
        self._width = 0
        self.path_type = 0
        self._pts = None

    @property
    def pts(self):
        return self._pts

    @pts.setter
    def pts(self, pts):

        if len(pts) < 2:
            raise Exception('The xy expects more then 2 pairs in path')
        self._pts = pts

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, width):
        if width % 2 != 0:
            raise Exception('The width should be even.')
        self._width = width

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['PATH']:
            raise exceptions.FormatError('Unexpected tag where PATH is expected:', rec_type)
        
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
                    raise exceptions.IncorrectDataSize('XY')
                p_num = int((size - 4) / 8)
                p_list = []
                for i in range(p_num):
                    x = read_integer(stream)
                    y = read_integer(stream)
                    p_list.append(Point(x, y))
                self.pts = p_list
            elif rec_type == RecordType['WIDTH']:
                self.width = read_integer(stream)
            elif rec_type == RecordType['PATHTYPE']:
                self.path_type = read_short(stream)
            else:
                stream.seek(size - 4, 1)
            size, rec_type, _ = read_one_record(stream)

    def bbox(self):
        """ Get the bounding rect of path.

        Returns
            (llpoint, (width, height)): the first elment is a Point which indicates the low left vertex,
            and the second element is a tuple which indicates the width and height of bounding rect.

        Raises
            Exception: The path has not been initialized."""
        if self.width == 0 or self.pts is None:
            raise Exception("The path has not been initialized correctly.")
        llx = urx = self.pts[0].x
        lly = ury = self.pts[0].y
        for pp in self.pts:
            if pp.x < llx:
                llx = pp.x
            if pp.x > urx:
                urx = pp.x
            if pp.y < lly:
                lly = pp.y
            if pp.y > ury:
                ury = pp.y
        # Extend the path
        for i in range(1, len(self.pts)):
            if self.pts[i-1].x == self.pts[i].x:    # vertical segment
                if self.pts[i].x - self.width / 2 < llx:
                    llx = self.pts[i].x - self.width / 2
                if self.pts[i].x + self.width / 2 > urx:
                    urx = self.pts[i].x + self.width / 2
            else:   # horizontal segment
                if self.pts[i].y - self.width / 2 < lly:
                    lly = self.pts[i].y - self.width / 2
                if self.pts[i].y + self.width / 2 > ury:
                    ury = self.pts[i].y + self.width / 2
        # Extend the end point
        if self.path_type > 0:
            if self.pts[0].x == self.pts[1].x:  # vertical begin segment
                if self.pts[0].y < self.pts[1].y and self.pts[0].y - self.width / 2 < lly:
                    lly = self.pts[0].y - self.width / 2
                elif self.pts[0].y > self.pts[1].y and self.pts[0].y + self.width / 2 > ury:
                    ury = self.pts[0].y + self.width / 2
            else:   # horizontal begin segment
                if self.pts[0].x < self.pts[1].x and self.pts[0].x - self.width / 2 < llx:
                    llx = self.pts[0].x - self.width / 2
                elif self.pts[0].x > self.pts[1].x and self.pts[0].x + self.width / 2 > urx:
                    urx = self.pts[0].x + self.width / 2
            if self.pts[-2].x == self.pts[-1].x:    # vertical end segment
                if self.pts[-2].y < self.pts[-1].y and self.pts[-1].y + self.width / 2 > ury:
                    ury = self.pts[-1].y + self.width / 2
                elif self.pts[-2].y > self.pst[-1].y and self.pts[-1].y - self.width / 2 < lly:
                    lly = self.pts[-1].y - self.width / 2
            else:
                if self.pts[-2].x < self.pts[-1].x and self.pts[-1].x + self.width / 2 > urx:
                    urx = self.pts[-1].x + self.width / 2
                elif self.pts[-2].x > self.pts[-1].x and self.pts[-1].x - self.width / 2 < llx:
                    llx = self.pts[-1].x - self.width / 2
        return (llx, lly), (urx - llx, ury - lly)




