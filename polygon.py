from elementbase import ElementBase


class Polygon(ElementBase):

    def __init__(self):
        super().__init__('BOUNDARY')
        self.eflags = 0
        self.layer = -1
        self.data_type = -1
        self.pts = []

