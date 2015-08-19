from datetime import datetime
import misc
import exceptions
from cell import *
from aref import *
from sref import *


class GDS(dict):

    def __init__(self):
        super().__init__()
        self.version = 0
        now = datetime.now()
        self.mod_year = now.year
        self.mod_month = now.month
        self.mod_day = now.day
        self.mod_hour = now.hour
        self.mod_minute = now.minute
        self.mod_second = now.second
        self.acc_year = now.year
        self.acc_month = now.month
        self.acc_day = now.day
        self.acc_hour = now.hour
        self.acc_minute = now.minute
        self.acc_second = now.second

        self.db_in_meter = 1.0e-9
        self.db_in_userunit = 1.0e-3

        self._cell_cache = {}

    def _cache(self, stream):
        self._cell_cache.clear()
        """Build the mapping between the cell data and the gds file."""

        size, rec_type, _ = misc.read_one_record(stream)
        if rec_type != misc.RecordType['HEADER']:
            raise exceptions.FormatError('Unexpected tag where HEADER is expected:', rec_type)
        elif size != 6:
            raise exceptions.IncorrectDataSize('The HEADER expects 6 bytes data.')
        self.version = misc.read_short(stream)

        size, rec_type, _ = misc.read_one_record(stream)
        if (rec_type != misc.RecordType['BGNLIB']):
            raise exceptions.FormatError('Unexpected tag where BGNLIB is expected:', rec_type)
        elif size != 28:
            raise exceptions.IncorrectDataSize('The BGNLIB expects 28 bytes data')
        self.mod_year = misc.read_short(stream)
        self.mod_month = misc.read_short(stream)
        self.mod_day = misc.read_short(stream)
        self.mod_hour = misc.read_short(stream)
        self.mod_minute = misc.read_short(stream)
        self.mod_second = misc.read_short(stream)
        self.acc_year = misc.read_short(stream)
        self.acc_month = misc.read_short(stream)
        self.acc_day = misc.read_short(stream)
        self.acc_hour = misc.read_short(stream)
        self.acc_minute = misc.read_short(stream)
        self.acc_second = misc.read_short(stream)

        size, rec_type, _ = misc.read_one_record(stream)
        while rec_type != misc.RecordType['ENDLIB']:
            if rec_type == misc.RecordType['LIBNAME']:
                self.lib_name = misc.read_string(stream, size - 4)
            elif rec_type == misc.RecordType['UNITS']:
                if (size != 20):
                    raise exceptions.IncorrectDataSize('The UNITS expects 20 bytes data')
                self.db_in_userunit = misc.read_float(stream)
                self.db_in_meter = misc.read_float(stream)
            elif rec_type == misc.RecordType['BGNSTR']:
                start_pos = stream.tell() - 4
                stream.seek(size - 4, 1)
                size, rec_type, _ = misc.read_one_record(stream)
                while rec_type != misc.RecordType['ENDSTR']:
                    if rec_type == misc.RecordType['STRNAME']:
                        self._cell_cache[misc.read_string(stream, size - 4)] = start_pos
                    else:
                        if size > 4:
                            # seek current
                            stream.seek(size - 4, 1)
                    size, rec_type, _ = misc.read_one_record(stream)
            else:
                raise exceptions.UnsupportedTagType(rec_type)
            size, rec_type, _ = misc.read_one_record(stream)

    def read(self, in_stream):
        self._cache(in_stream)
        self.clear()
        for name, pos in self._cell_cache.items():
            cell = Cell(name)
            in_stream.seek(pos)
            cell.read(in_stream)
            self[name] = cell

    def build_cell_links(self):
        for name, cell in self.items():
            for element in cell:
                if isinstance(element, SRef) or isinstance(element, ARef):
                    if element.sname in self:
                        element.refer_to = self[element.sname]
                        if cell not in self[element.sname].refer_by:
                            self[element.sname].refer_by.append(cell)




if __name__ == "__main__":
    file_name = "c:/M1necking_001.db"
    try:
        stream = open(file_name, 'rb')
        gds = GDS()
        gds.read(stream)
    except FileNotFoundError:
        print("File not found")
    except exceptions.EndOfFileError:
        print("The file is not completed.")
    except exceptions.IncorrectDataSize as e:
        print(e.args[0])
    except exceptions.UnsupportedTagType as e:
        print("Unsupported tag type ", e.args[0])
    except exceptions.FormatError as e:
        print(e.args[0], e.args[1])
    finally:
        stream.close()
