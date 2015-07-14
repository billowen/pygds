from elementbase import ElementBase


class Path(ElementBase):

    def __init__(self):
        super().__init__('PATH')

        self.eflags = 0
        self.layer = -1
        self.data_type = -1
        self.width = 0
        self.path_type = 0
        self.pts = []
