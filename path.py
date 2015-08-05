from elementbase import ElementBase
from misc import *
import exceptions

class Path(ElementBase):

    def __init__(self):
        super().__init__('PATH')

        self.eflags = 0
        self.layer = -1
        self.data_type = -1
        self.width = 0
        self.path_type = 0
        self.pts = None

    @property
    def pts(self):
        return self._pts

    @pts.setter
    def pts(self, pts):
        if len(pts) < 2:
            raise exception('the xy expects more then 2 pairs in path') 
        self._pts = pts

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
            elif rec_type == RecordType['WIDTH']:
                self.width = read_integer(stream)
            elif rec_type == RecordType['PATHTYPE']:
                self.path_type = read_short(stream)
            else:
                stream.seek(size - 4, 1)
            size, rec_type, _ = read_one_record(stream)
