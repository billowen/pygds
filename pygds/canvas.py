from PySide.QtGui import *
from polygon import Polygon
from path import Path
from aref import ARef
from sref import SRef
from graphicsitems import *
import os

class MyRect(QGraphicsRectItem):
    def __init__(self, x, y, w, h, scene=None):
        super().__init__(x, y, w, h, scene)

    def paint(self, painter, option, widget):
        pen = QPen(QColor(0, 0, 0))
        if option.state & QStyle.State_Selected:
            pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        brush = QBrush(QColor(12, 34, 53))
        brush.setStyle(Qt.HorPattern)
        painter.setBrush(brush)
        painter.drawRect(self.rect())


class Canvas(QGraphicsView):

    def __init__(self, cell, parent=None):
        super().__init__(parent)
        self.cell = cell
        self.setCacheMode(QGraphicsView.CacheBackground)
        scene = QGraphicsScene()
        self.setScene(scene)
        self.scale(1, -1)
        # self.scene().addItem(MyRect(10,10,10,10))
        for element in self.cell:
           # if isinstance(element, SRef):
           #     self.scene().addItem(SRefViewItem(element))
           if isinstance(element, Polygon):
               self.scene().addItem(PolygonViewItem(element))
           elif isinstance(element, Path):
               self.scene().addItem(PathViewItem(element))
           elif isinstance(element, SRef):
               self.scene().addItem(SRefViewItem(element))
           elif isinstance(element, ARef):
               self.scene().addItem(ARefViewItem(element))
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    #def resizeEvent(self, *args, **kwargs):
    #    self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)

    def wheelEvent(self, evt):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        old_pos = self.mapToScene(evt.pos())
        if evt.delta() > 0:
            zoom_fact = zoom_in_factor
        else:
            zoom_fact = zoom_out_factor
        self.scale(zoom_fact, zoom_fact)
        new_pos = self.mapToScene(evt.pos())
        move = new_pos - old_pos
        self.translate(move.x(), move.y())



if __name__ == '__main__':
    file_name = "transistor_hisilicon_28_nm_RF_20150322.xsmc.db"
    print(os.getcwd())
    gds = GDS()
    with open(file_name, 'rb') as stream:
        gds.read(stream)
        gds.build_cell_links()
    app = QApplication(sys.argv)
    canvas = Canvas(gds["CELL_007"])
    mainwin = QMainWindow()
    mainwin.setCentralWidget(canvas)
    mainwin.show()
    sys.exit(app.exec_())
    # if os.path.exists(file_name) is True:
    #     try:
    #
    #     except FileNotFoundError:
    #         print("File not found")
    #     except exceptions.EndOfFileError:
    #         print("The file is not completed.")
    #     except exceptions.IncorrectDataSize as e:
    #         print(e.args[0])
    #     except exceptions.UnsupportedTagType as e:
    #         print("Unsupported tag type ", e.args[0])
    #     except exceptions.FormatError as e:
    #         print(e.args[0], e.args[1])
    #     finally:
    #         stream.close()

