from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPolygon
from PyQt5.QtWidgets import QCommonStyle, QStyle, QStyleOption, QWidget

from logger import logged, logger


class MyStyle(QCommonStyle):

    def drawPrimitive(
        self
        , primitive_element: QStyle.PrimitiveElement
        , option: QStyleOption
        , painter: QPainter
        , widget: QWidget = None
    ):

        # if primitive_element in [QStyle.PE_IndicatorSpinUp, QStyle.PE_IndicatorSpinDown]:
        #     self.drawPrimitiveIndicatorSpin(primitive_element, option, painter, widget)
        # else:
        #     super().drawPrimitive(primitive_element, option, painter, widget)

        super().drawPrimitive(primitive_element, option, painter, widget)

    @logged(disabled=False)
    def drawPrimitiveIndicatorSpin(
        self
        , primitive_element: QStyle.PrimitiveElement
        , option: QStyleOption
        , painter: QPainter
        , widget: QWidget = None
    ):
        points = QPolygon(3)

        x, y = option.rect.x(), option.rect.y()
        w, h = option.rect.width() // 2, option.rect.height() // 2

        logger.debug(f"{x}, {y} -- {w}, {h}")

        x += (option.rect.width() - w) // 2
        y += (option.rect.height() - h) // 2

        # if element == QStyle.PE_IndicatorSpinUp:
        points[0] = QPoint(x, y + h)
        points[1] = QPoint(x + w, y + h)
        points[2] = QPoint(x + w // 2, y)
        # else:

        if option.state & QStyle.State_Enabled:
            painter.setPen(option.palette.mid().color())
            painter.setBrush(option.palette.buttonText())
        else:
            painter.setPen(option.palette.buttonText().color())
            painter.setBrush(option.palette.mid())

        painter.drawPolygon(points)
