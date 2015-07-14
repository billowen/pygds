from misc import Point
from elementbase import ElementBase

class SRef(ElementBase):

    def __init__(self):

        super().__init__('SREF')
        self.eflags = 0
        self.strans = 0
        self.sname = ""
        self.angle = 0.0
        self.mag = 1.0
        self.pt = Point()
        slef.refer_to = None
