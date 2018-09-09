import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.ui.base import TScrollArea
from src.ui.home.t_scroll_wgt import TScrollWidget


class THomeScrollArea(TScrollArea):
    """Show several tables that contain time slots"""

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        # self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setWidget(TScrollWidget())
        self.setWidgetResizable(True)

    @pyqtSlot()
    def handle_show_next_shortcut(self):

        self.widget().request_next()

    def event(self, event: QEvent):

        # if isinstance(event, QResizeEvent):
        #     self.logger.info(f'ScrollArea ResizeEvent {event.oldSize()} -> {event.size()}')
        # elif isinstance(event, QMoveEvent):
        #     self.logger.info(f'ScrollArea MoveEvent {event.oldPos()} -> {event.pos()}')
        # else:
        #     self.logger.info(f'ScrollArea {event}')

        return super().event(event)
