from polygon import *
from cell import *
from path import *
from PySide.QtCore import *
from PySide.QtGui import *
from random import randint


def paint_polygon(painter, data):
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    painter.pen().setColor(QColor(r, g, b))
    polygon = QPolygonF()
    for v in data.pts:
        polygon.append(QPointF(v.x, v.y))
    painter.drawPolygon(polygon)


def create_qpath(data):
    path = QPainterPath()
    path_type_sign = 0
    if data.path_type > 0:
        path_type_sign = 1
    if data.pts[0].x == data.pts[1].x:  # vertical begin
        _width = data.width
        _height = abs(data.pts[1].y - data.pts[0].y) + data.width / 2 * (1 + path_type_sign)
        if data.pts[0].y < data.pts[1].y:
            _x = data.pts[0].x - data.width / 2
            _y = data.pts[0].y - path_type_sign * data.width / 2
            path.addRect(_x, _y, _width, _height)
        else:
            _x = data.pts[1].x - data.width / 2
            _y = data.pts[1].y - data.width / 2
            path.addRect(_x, _y, _width, _height)
    else:   # horizontal begin
        _width = abs(data.pts[1].x - data.pts[0].x) + data.width / 2 * (1 + path_type_sign)
        _height = data.width
        if data.pts[0].x < data.pts[1].x:
            _x = data.pts[0].x - path_type_sign * data.width / 2
            _y = data.pts[0].y - data.width / 2
            path.addRect(_x, _y, _width, _height)
        else:
            _x = data.pts[1].x - data.width / 2
            _y = data.pts[1],y - data.width / 2
            path.addRect(_x, _y, _width, _height)

    _tmp_l = list(range(len(data.pts)))
    for i in _tmp_l[1:-2]:
        if data.pts[i].x == data.pts[i+1].x:    # vertical segment
            _width = data.width
            _height = abs(data.pts[i].y - data.pts[i+1].y) + data.width
            _low_point = data.pts[i]
            if data.pts[i].y > data.pts[i+1].y:
                _low_point = data.pts[i+1]
            _x = _low_point.x - data.width / 2
            _y = _low_point.y - data.width / 2
            path.addRect(_x, _y, _width, _height)
        else:   # horizontal segment
            _width = abs(data.pts[i].x - data.pts[i+1].x) + data.width
            _height = data.width
            _low_point = data.pts[i]
            if data.pts[i].x > data.pts[i+1].x:
                _low_point = data.pts[i+1]
            _x = _low_point.x - data.width / 2
            _y = _low_point.y - data.width / 2
            path.addRect(_x, _y, _width, _height)

    if data.pts[-2].x == data.pts[-1].x:    # vertical end
        _width = data.width
        _height = abs(data.pts[-2].y - data.pts[-1].y) + data.width / 2 * (1 + path_type_sign)
        if data.pts[-2].y < data.pts[-1].y:
            _x = data.pts[-2].x - data.width / 2
            _y = data.pts[-2].y - data.width / 2
            path.addRect(_x, _y, _width, _height)
        else:
            _x = data.pts[-1].x - data.width / 2
            _y = data.pts[-1].y - path_type_sign * data.width / 2
            path.addRect(_x, _y, _width, _height)
    else:   # horizontal end
        _width = abs(data.pts[-2].x - data.pts[-1].x) + data.width / 2 * (1 + path_type_sign)
        _height = data.width
        if data.pts[-2].x < data.pts[-1].x:
            _x = data.pts[-2].x - data.width / 2
            _y = data.pts[-2].y - data.width / 2
            path.addRect(_x, _y, _width, _height)
        else:
            _x = data.pts[-1].x - path_type_sign * data.width / 2
            _y = data.pts[-1].y - data.width / 2
            path.addRect(_x, _y, _width, _height)
    path.setFillRule(Qt.WindingFill)
    return path


def paint_path(painter, data):
    # The path has not been initialize correctly.
    if data.width == 0 or data.pts is None:
        return
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    painter.pen().setColor(QColor(r, g, b))
    painter.brush().setColor(QColor(r, g, b))
    painter.fillPath(create_qpath(data), QColor(r, g, b))


def paint_cell(painter, cell, level=-1, offset_x=0, offset_y=0, mag=1.0, angle=0, reflect=False):
    transform_back = painter.QTransform
    transform = QTransform()
    if reflect is True:
        transform.scale(1, -1)
    transform.scale(mag, mag)
    transform.rotate(angle)
    transform.translate(offset_x, offset_y)
    painter.setTransform(transform, True)

    if level < 0:
        level = 99
    if level == 0:
        r = randint(0, 255)
        g = randint(0, 255)
        b = randint(0, 255)
        painter.pen().setColor(QColor(r, g, b))
        painter.brush().setColor(QColor(r, g, b))
        




def paint_sref(painter, data):
    r = randint(0, 255)
    g = randint(0, 255)
    b = randint(0, 255)
    painter.pen().setColor(QColor(r, g, b))
    painter.brush().setColor(QColor(r, g, b))



