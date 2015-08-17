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
                self.eflags = read_bitarray(stream)
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
            (llpoint, (width, height)): the first elment is a Point which indicates the low left vertex,
            and the second element is a tuple which indicates the width and height of bounding rect.

        Raises
            Exception: The SREF has not been initialized."""
        if self.refer_to is None:
            raise Exception('The SREF has not been initialized correctly.')

        transform = QTransform()
        if self.reflect is True:
            transform.scale(1, -1)
        transform.scale(self.mag, self.mag)
        transform.rotate(self.angle)
        transform.translate(self.pt.x, self.pt.y)

        (_x, _y), (_width, _height) = self.refer_to.bbox()
        rect = QRect(_x, _y, _width, _height)
        rect2 = transform.mapRect(rect)
        return (rect2.x(), rect2.y()), (rect2.width(), rect2.height())