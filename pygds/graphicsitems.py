from PySide.QtGui import *
from PySide.QtCore import *
from polygon import Polygon
from path import Path
from aref import ARef
from sref import SRef
from gds import GDS
from graphicsutilities import *
from cell import *
import sys
import os.path


class PolygonViewItem(QGraphicsItem):

    def __init__(self, data):
        super().__init__()

        if not isinstance(data, Polygon):
            raise Exception('The PolygonViewItem uses a Polygon as the initializing data.')

        self._data = data
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def boundingRect(self):
        box = self._data.bbox()
        return QRectF(box.x, box.y, box.width, box.height)

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
        box = self._data.bbox()
        return QRectF(box.x, box.y, box.width, box.height)

    def paint(self, painter, option, widget):
        pen = QPen(QColor(0, 0, 0))
        if option.state & QStyle.State_Selected:
            pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        paint_path(painter, self._data)

    def shape(self):
        return create_qpath(self._data)


class ARefViewItem(QGraphicsItem):

    def __init__(self, data):
        super().__init__()
        if not isinstance(data, ARef):
            raise Exception('The ARefViewItem uses a ARef as the initializing data.')
        self._data = data
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.show_level = -1

    def boundingRect(self):
        box = self._data.bbox()
        return QRectF(box.x, box.y, box.width, box.height)

    def paint(self, painter, option, widget):
        pen = QPen(QColor(0, 0, 0))
        if option.state & QStyle.State_Selected:
            pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        paint_aref(painter, self._data, -1)


class SRefViewItem(QGraphicsItem):

    def __init__(self, data):
        super().__init__()
        if not isinstance(data, SRef):
            raise Exception('The SRefViewItem uses a SRef as the initializing data.')
        self._data = data
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.show_level = -1

    def boundingRect(self):
        box = self._data.bbox()
        return QRectF(box.x, box.y, box.width, box.height)

    def paint(self, painter, option, widget):
        pen = QPen(QColor(0, 0, 0))
        if option.state & QStyle.State_Selected:
            pen.setStyle(Qt.DotLine)
        painter.setPen(pen)
        paint_sref(painter, self._data, -1)



