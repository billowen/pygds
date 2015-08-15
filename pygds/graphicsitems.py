from PySide.QtGui import *
from PySide.QtCore import *
from polygon import *
from path import *
from path import Path
from graphicsutilities import *
import sys
import pdb


class PolygonViewItem(QGraphicsItem):

    def __init__(self, data):
        super().__init__()

        if not isinstance(data, Polygon):
            raise Exception('The PolygonViewItem uses a Polygon as the initializing data.')

        self._data = data
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        xy, size = self._data.bbox()
        return QRectF(QPointF(xy[0], xy[1]), QSizeF(size[0], size[1]))

    def paint(self, painter, option, widget):
        pen = QPen(QColor(0, 0, 0))
        if option.state & QStyle.State_Selected:
            pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        paint_polygon(painter, self._data)

    def shape(self):
        path = QPainterPath()
        polygon = QPolygonF()
        for v in self._data.pts:
            polygon.append(QPointF(v.x, v.y))
        path.addPolygon(polygon)
        return path


class PathViewItem(QGraphicsItem):

    def __init__(self, data):
        super().__init__()
        if not isinstance(data, Path):
            raise Exception('The PathViewItem uses a Path as the initializing data.')
        self._data = data
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        xy, size = self._data.bbox()
        return QRectF(QPointF(xy[0], xy[1]), QSizeF(size[0], size[1]))

    def paint(self, painter, option, width):
        pen = QPen(QColor(0, 0, 0))
        if option.state & QStyle.State_Selected:
            pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        paint_path(painter, self._data)

    def shape(self):
        return create_qpath(self._data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    p_list = [Point(50, 50), Point(50, 100), Point(100, 100), Point(100, 200)]
    path = Path()
    path.pts = p_list
    path.width = 10
    p_item = PathViewItem(path)
    scene = QGraphicsScene()
    view = QGraphicsView()
    view.setScene(scene)
    view.scale(1, -1)
    scene.addItem(p_item)

    mainwin = QMainWindow()
    mainwin.setCentralWidget(view)
    mainwin.show()
    sys.exit(app.exec_())

