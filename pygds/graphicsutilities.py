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
    init_painter(painter)
    painter.fillPath(create_qpath(data), painter.brush())


def paint_sref(painter, data, level=-1):
    paint_cell(painter, data.refer_to, level,
               data.pt.x, data.pt.y,  data.mag, data.angle, data.reflect)


def _cal_distance(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return sqrt(dx*dx + dy*dy)


def paint_aref(painter, data, level=-1):
    transform_back = painter.transform()
    pitch_x = _cal_distance(data.pts[0], data.pts[1]) / data.col
    pitch_y = _cal_distance(data.pts[0], data.pts[2]) / data.row
    for i in range(data.row):
        for j in range(data.col):
            cur_x = data.pts[0].x + j * pitch_x
            cur_y = data.pts[0].y + i * pitch_y
            cur_transform = QTransform()
            if data.reflect is True:
                cur_transform.scale(1, -1)
            cur_transform.scale(data.mag, data.mag)
            cur_transform.translate(cur_x, cur_y)
            cur_transform.translate(-data.pts[0].x, -data.pts[0].y)
            cur_transform.rotate(data.angle)
            cur_transform.translate(data.pts[0].x, data.pts[0].y)
            painter.setTransform(cur_transform, True)
            paint_cell(painter, data.refer_to, level)
            painter.setTransform(transform_back)


def paint_cell(painter, cell, level=-1, offset_x=0, offset_y=0, mag=1.0, angle=0, reflect=False):
    transform_back = painter.transform()
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
        init_painter(painter)
        cell_box = cell.bbox()
        rect = QRect(cell_box.x, cell_box.y, cell_box.width, cell_box.height)
        painter.drawRect(rect)
        painter.drawText(rect, Qt.AlignCenter, cell.name)
    else:
        init_painter(painter)
        for element in cell.elements:
            if isinstance(element, Polygon):
                paint_polygon(painter, element)
            elif isinstance(element, Path):
                paint_path(painter, element)
            elif isinstance(element, ARef):
                paint_aref(painter, element, level-1)
            elif isinstance(element, SRef):
                paint_sref(painter, element, level-1)

    painter.setTransform(transform_back)




