from misc import Point
from elementbase import ElementBase


class Text(ElementBase):

    def __init__(self):
        super().__init__("TEXT")

        self.eflags = 0
        self.layer = -1
        self.text_type = -1
        self.presentation = 0
        self.strans = 0
        self.string = ""
        self.pt = Point()
