from elementbase import ElementBase


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
        self.pts = []
        self.refer_to = None
