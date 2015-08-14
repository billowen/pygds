from misc import *
from elementbase import ElementBase
import exceptions


class Text(ElementBase):

    def __init__(self):
        super().__init__("TEXT")

        self.eflags = 0
        self.layer = -1
        self.text_type = -1
        self.presentation = 0
        self.strans = 0
        self.string = ""
        self.pt = None

    def read(self, stream):
        size, rec_type, _ = read_one_record(stream)
        if rec_type != RecordType['TEXT']:
            raise exceptions.FormatError('Unexpected tag where TEXT is expected:', rec_type)

        size, rec_type, _ = read_one_record(stream)
        while rec_type != RecordType['ENDEL']:
            if rec_type == RecordType['EFLAGS']:
                self.eflags = read_bitarray(stream)
            elif rec_type == RecordType['LAYER']:
                self.layer = read_short(stream)
            elif rec_type == RecordType['TEXTTYPE']:
                self.text_type = read_short(stream)
            elif rec_type == RecordType['PRESENTATION']:
                self.presentation = read_bitarray(stream)
            elif rec_type == RecordType['STRANS']:
                self.strans = read_bitarray(stream)
            elif rec_type == RecordType['STRING']:
                self.string = read_string(stream, size - 4)
            elif rec_type == RecordType['XY']:
                x = read_integer(stream)
                y = read_integer(stream)
                self.pt = Point(x, y)
            else:
                stream.seek(size - 4, 1)
            size, rec_type, _ = read_one_record(stream)
