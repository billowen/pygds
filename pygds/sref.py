from misc import *
import exceptions
from elementbase import ElementBase
from PySide.QtGui import QTransform
from PySide.QtCore import QRect

class SRef(ElementBase):

    def __init__(self):

        super().__init__('SREF')
        self.eflags = 0
        self.strans = 0
        self.sname = ""
        self.angle = 0.0
        self.mag = 1.0
        self.pt = None
        self.refer_to = None

    @property
    def reflect(self):
        return bool(self.strans & 0x8000)

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['SREF']:
            raise exceptions.FormatError('Unexpected tag where SREF is expected:', rec_type)

        size, rec_type, _ = read_one_record(stream)
        while rec_type != RecordType['ENDEL']:
            if rec_type == RecordType['EFLAGS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['STRANS']:
                self.strans = read_bitarray(stream)
            elif rec_type == RecordType['SNAME']:
                self.sname = read_string(stream, size - 4)
            elif rec_type == RecordType['ANGLE']:
                self.angle = read_float(stream)
            elif rec_type == RecordType['MAG']:
                self.mag = read_float(stream)
            elif rec_type == RecordType['XY']:
                x = read_integer(stream)
                y = read_integer(stream)
                self.pt = Point(x, y)
            else:
                stream.seek(size - 4, 1)
            size, rec_type, _ = read_one_record(stream)

    def bbox(self):
        """ Get the bounding rect of a SREF.

        Returns
            bbox: the BBox which indicates the bbox of current gds element or none if failed to calculate the bbox.
        """
        if self.refer_to is None or self.pt is None:
            return None

        ref_bbox = self.refer_to.bbox()
        if ref_bbox is None:
            return None

        reflect_transform = QTransform()
        if self.reflect is True:
            reflect_transform.scale(1, -1)
        mag_transform = QTransform().scale(self.mag, self.mag)
        rotate_transform = QTransform().rotate(self.angle)
        shift_transform = QTransform().translate(self.pt.x, self.pt.y)
        transform = reflect_transform * mag_transform * rotate_transform * shift_transform

        rect = QRect(ref_bbox.x, ref_bbox.y, ref_bbox.width, ref_bbox.height)
        rect2 = transform.mapRect(rect)
        return BBox(rect2.x(), rect2.y(), rect2.width(), rect2.height())
