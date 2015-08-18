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

    def bbox(self):
        """ Get the bounding rect of a AREF.

        Returns
            bbox: the Rect which indicates the bbox of current gds element or none if failed to calculate the bbox.
        """
        if self.refer_to is None or self.pts is None or self.row <= 0 or self.col <= 0 or len(self.pts) != 3:
            return None
        pitch_x = _cal_distance(self.pts[0], self.pts[1]) / self.col
        pitch_y = _cal_distance(self.pts[0], self.pts[2]) / self.row

        ref_bbox = self.refer_to.bbox()
        if ref_bbox is None:
            return None

        rect1 = QRect(ref_bbox.x, ref_bbox.y, ref_bbox.width, ref_bbox.height)
        transform = QTransform()
        if self.reflect is True:
            transform.scale(1, -1)
        transform.scale(self.mag, self.mag)
        transform.translate(self.pts[0].x, self.pts[0].y)
        rect2 = transform.mapRect(rect1)
        transform.translate(pitch_x * (self.col - 1), 0)
        rect3 = transform.mapRect(rect1)
        transform.translate(0, pitch_y * (self.row - 1))
        rect4 = transform.mapRect(rect1)

        llx = rect2.x()
        lly = rect2.y()
        urx = rect2.x() + rect2.width()
        ury = rect2.y() + rect2.height()
        if rect3.x() < llx:
            llx = rect3.x()
        if rect3.y() < lly:
            lly = rect3.y()
        if rect3.x() + rect3.width() > urx:
            urx = rect3.x() + rect3.width()
        if rect3.y() + rect3.height() > ury:
            ury = rect3.y() + rect3.height()

        if rect4.x() < llx:
            llx = rect4.x()
        if rect4.y() < lly:
            lly = rect4.y()
        if rect4.x() + rect4.width() > urx:
            urx = rect4.x() + rect4.width()
        if rect4.y() + rect4.height() > ury:
            ury = rect4.y() + rect4.height()

        aref_rect = QRect(llx, lly, urx - llx, ury - lly)
        rotate_transform = QTransform()
        rotate_transform.translate(-self.pts[0].x, -self.pts[0].y)
        rotate_transform.rotate(self.angle)
        rotate_transform.translate(self.pts[0].x, self.pts[0].y)
        rect5 = rotate_transform.mapRect(aref_rect)
        return BBox(rect5.x(), rect5.y(), rect5.width(), rect5.height())





