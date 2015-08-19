from PySide.QtGui import *
from polygon import Polygon
from path import Path
from aref import ARef
from sref import SRef
from graphicsitems import *
import os


class Canvas(QGraphicsView):

    def __init__(self, cell):
        super().__init__()
        self.cell = cell
        scene = QGraphicsScene()
        self.setScene(scene)
        self.scale(1, -1)
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

    def resizeEvent(self, *args, **kwargs):
        self.fitInView(self.scene().sceneRect(), Qt.KeepAspectRatio)


if __name__ == '__main__':
    file_name = "transistor_hisilicon_28_nm_RF_20150322.xsmc.db"
    print(os.getcwd())
    gds = GDS()
    with open(file_name, 'rb') as stream:
        gds.read(stream)
        gds.build_cell_links()
    app = QApplication(sys.argv)
    canvas = Canvas(gds["105lvtnmos1_001"])
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

