from polygon import *
from cell import *
from path import *
from PySide.QtCore import *
from PySide.QtGui import *
from random import randint


def init_painter(painter):
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    painter.pen().setColor(QColor(r, g, b))
    painter.brush().setColor(QColor(r, g, b))


def paint_polygon(painter, data):
    init_painter(painter)
    polygon = QPolygonF()
    for v in data.pts:
        polygon.append(QPointF(v.x, v.y))
    painter.drawPolygon(polygon)


def create_qpath(data):
    path = QPainterPath()
    path.moveTo(data.pts[0].x, data.pts[0].y)
    for p in data.pts[1:]:
        path.lineTo(p.x, p.y)
    stroker = QPainterPathStroker()
    stroker.setJoinStyle(Qt.MiterJoin)
    stroker.setCapStyle(Qt.FlatCap)
    stroker.setWidth(data.width)
    return stroker.createStroke(path)


def paint_path(painter, data):
    # The path has not been initialize correctly.
    if data.width == 0 or data.pts is None:
        return
    init_painter(painter)
    painter.drawPath(create_qpath(data))


def paint_sref(painter, data, level=-1):
    paint_cell(painter, data.refer_to, level,
               data.pt.x, data.pt.y,  data.mag, data.angle, data.reflect)


def paint_aref(painter, data, level=-1):
    row_pitch_x = (data.pts[2].x - data.pts[0].x) / data.row
    row_pitch_y = (data.pts[2].y - data.pts[0].y) / data.row
    col_pitch_x = (data.pts[1].x - data.pts[0].x) / data.col
    col_pitch_y = (data.pts[1].y - data.pts[0].y) / data.col
    for i in range(data.row):
        row_offset_x = data.pts[0].x + i * row_pitch_x
        row_offset_y = data.pts[0].y + i * row_pitch_y
        for j in range(data.col):
            cur_x = row_offset_x + j * col_pitch_x
            cur_y = row_offset_y + j * col_pitch_y
            paint_cell(painter,
                       cell=data.refer_to,
                       level=level,
                       offset_x=cur_x, offset_y=cur_y,
                       mag=data.mag, angle=data.angle, reflect=data.reflect)


def paint_cell(painter, cell, level=-1, offset_x=0, offset_y=0, mag=1.0, angle=0, reflect=False):
    transform_back = painter.transform()
    reflect_transform = QTransform()
    if reflect is True:
        reflect_transform.scale(1, -1)
    mag_transform = QTransform().scale(mag, mag)
    rotate_transform = QTransform().rotate(angle)
    shift_transform = QTransform().translate(offset_x, offset_y)
    transform = reflect_transform * mag_transform * rotate_transform * shift_transform
    painter.setTransform(transform, True)

    if level < 0:
        level = 99
    if level == 0:
        init_painter(painter)
        cell_box = cell.bbox()
        rect = QRect(cell_box.x, cell_box.y, cell_box.width, cell_box.height)
        painter.drawRect(rect)
        painter.drawText(rect, Qt.AlignCenter, cell.name)
    else:
        init_painter(painter)
        for element in cell:
            if isinstance(element, Polygon):
                paint_polygon(painter, element)
            elif isinstance(element, Path):
                paint_path(painter, element)
            elif isinstance(element, ARef):
                paint_aref(painter, element, level-1)
            elif isinstance(element, SRef):
                paint_sref(painter, element, level-1)

    painter.setTransform(transform_back)




