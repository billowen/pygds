from elementbase import ElementBase
from misc import *
from math import *
import exceptions
from PySide.QtGui import QTransform
from PySide.QtCore import QRect


def _cal_distance(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return sqrt(dx*dx + dy*dy)


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
            raise Exception('the xy expects 3 pairs for aref.')
        self._pts = pts

    @property
    def reflect(self):
        return bool(self.strans & 0x8000)

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['AREF']:
            raise exceptions.FormatError('Unexpected tag where AREF is expected:', rec_type)

        size, rec_type, _ = read_one_record(stream)
        while rec_type != RecordType['ENDEL']:
            if rec_type == RecordType['EFLAGS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['STRANS']:
                self.strans = read_bitarray(stream)
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

    def bbox(self):
        """ Get the bounding rect of a AREF.

        Returns
            bbox: the Rect which indicates the bbox of current gds element or none if failed to calculate the bbox.
        """
        if self.refer_to is None or self.pts is None or self.row <= 0 or self.col <= 0 or len(self.pts) != 3:
            return None
        row_pitch_x = (self.pts[2].x - self.pts[0].x) / self.row
        row_pitch_y = (self.pts[2].y - self.pts[0].y) / self.row
        col_pitch_x = (self.pts[1].x - self.pts[0].x) / self.col
        col_pitch_y = (self.pts[1].y - self.pts[0].y) / self.col

        ref_bbox = self.refer_to.bbox()
        if ref_bbox is None:
            return None

        rect1 = QRect(ref_bbox.x, ref_bbox.y, ref_bbox.width, ref_bbox.height)
        reflect_transform = QTransform()
        if self.reflect is True:
            reflect_transform.scale(1, -1)
        mag_transform = QTransform().scale(self.mag, self.mag)
        rotate_transform = QTransform().rotate(self.angle)
        shift_transforms = [QTransform().translate(self.pts[0].x, self.pts[0].y),
                            QTransform().translate(self.pts[0].x + col_pitch_x * (self.col-1),
                                                   self.pts[0].y + col_pitch_y * (self.col-1)),
                            QTransform().translate(self.pts[0].x + row_pitch_x * (self.row-1),
                                                   self.pts[0].y + row_pitch_y * (self.row-1)),
                            QTransform().translate(self.pts[0].x
                                                   + row_pitch_x * (self.row-1)
                                                   + col_pitch_x * (self.col-1),
                                                   self.pts[0].y
                                                   + row_pitch_y * (self.row-1)
                                                   + col_pitch_y * (self.col-1))]

        llx = lly = GDS_MAX_INT
        urx = ury = GDS_MIN_INT
        for shift in shift_transforms:
            transform = reflect_transform*mag_transform*rotate_transform*shift
            map_rect = transform.mapRect(rect1)
            if map_rect.x() < llx:
                llx = map_rect.x()
            if map_rect.y() < lly:
                lly = map_rect.y()
            if map_rect.x() + map_rect.width() > urx:
                urx = map_rect.x() + map_rect.width()
            if map_rect.y() + map_rect.height() > ury:
                ury = map_rect.y() + map_rect.height()

        return BBox(llx, lly, urx - llx, ury - lly)





