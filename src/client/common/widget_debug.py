from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from common import event_type_to_str, size_policy_to_str
from logger import logged, logger


class WidgetDebug(QWidget):
    """
    Contains overridden methods that will self-log their calls and (some) parameters.

    You should copy paste the methods below into any widget that you want to debug.
    """

    @logged(disabled=False)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @logged(disabled=False)
    def setLayout(self, layout: QLayout):
        super().setLayout(layout)

    @logged(disabled=False)
    def show(self):
        super().show()

    @logged(disabled=False)
    def hide(self):
        super().hide()

    @logged(disabled=False)
    def setVisible(self, visible: bool):
        super().setVisible(visible)

    @logged(disabled=False)
    def moveEvent(self, event: QMoveEvent):
        logger.debug(f"{event.oldPos()} -> {event.pos()}")
        super().moveEvent(event)

    @logged(disabled=False)
    def resizeEvent(self, event: QResizeEvent):
        logger.debug(f"{event.oldSize()} -> {event.size()}")
        super().resizeEvent(event)

    @logged(disabled=False)
    def showEvent(self, event: QShowEvent):
        super().showEvent(event)

    @logged(disabled=False)
    def hideEvent(self, event: QHideEvent):
        super().hideEvent(event)

    @logged(disabled=True)
    def paintEvent(self, event: QPaintEvent):
        logger.debug(f"{event.rect()}")
        super().paintEvent(event)

    @logged(disabled=False)
    def event(self, event: QEvent) -> bool:
        logger.debug(f"{self.__class__.__name__}.event({event_type_to_str(event.type())})")
        return super().event(event)

    @logged(disabled=False)
    def width(self):
        return super().width()

    @logged(disabled=False)
    def height(self):
        return super().height()

    @logged(disabled=False)
    def geometry(self) -> QRect:
        return super().geometry()

    @logged(disabled=False)
    def setGeometry(self, x: int, y: int, width: int, height: int):
        super().setGeometry(x, y, width, height)

    @logged(disabled=False)
    def updateGeometry():
        super().updateGeometry()

    @logged(disabled=False)
    def layout() -> QLayout:
        super().layout()

    @logged(disabled=False)
    def setLayout(self, layout: QLayout):
        super().setLayout(layout)

    @logged(disabled=False)
    def ensurePolished(self):
        super().ensurePolished()

    @logged(disabled=False)
    def size(self) -> QSize:
        return super().size()

    @logged(disabled=False)
    def sizeHint(self) -> QSize:
        return super().sizeHint()

    @logged(disabled=False)
    def minimumSizeHint(self) -> QSize:
        return super().minimumSizeHint()

    @logged(disabled=False)
    def maximumSizeHint(self) -> QSize:
        return super().maximumSizeHint()

    @logged(disabled=False)
    def minimumSize(self) -> QSize:
        return super().minimumSize()

    @logged(disabled=False)
    def setMinimumSize(self, *args, **kwargs):
        return super().setMinimumSize(*args, **kwargs)

    @logged(disabled=False)
    def maximumSize(self) -> QSize:
        return super().maxiumsSize()

    @logged(disabled=False)
    def setmaximumSize(self, *args, **kwargs):
        return super().setMaximumSize(*args, **kwargs)

    @logged(disabled=False)
    def sizePolicy(self) -> QSizePolicy:
        return super().sizePolicy()

    @logged(disabled=False)
    def setSizePolicy(self, *args, **kwargs):
        return super().setSizePolicy(*args, **kwargs)

    @logged(disabled=False)
    def baseSize(self):
        super().baseSize()

    @logged(disabled=False)
    def setBaseSize(self, width: int, height: int):
        super().setBaseSize(width, height)

    @logged(disabled=False)
    def adjustSize(self):
        super().adjustSize()

    @logged(disabled=False)
    def contentsRect(self):
        super().contetsRect()

    @logged(disabled=False)
    def frameGeometry(self) -> QRect:
        super().frameGeometry()

    @logged(disabled=False)
    def _print_self_report(self):
        logger.debug(f"width and height: ({self.width()}, {self.height()})")
        logger.debug(f"geometry: {self.geometry()}")

        size_policy = self.sizePolicy()
        hpolicy = size_policy_to_str(size_policy.horizontalPolicy())
        vpolicy = size_policy_to_str(size_policy.verticalPolicy())
        logger.debug(f"size policy details: {hpolicy}, {vpolicy}")
