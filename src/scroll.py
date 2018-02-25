import datetime
import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.slot import TTableModel, TTableView
from src.types import LoadFailed
from src.utils import logged


class TScrollWidget(QWidget):
    '''
    Provide the top-level widget for the scroll-enabled area

    This widget should add/remove incoming SlotTableView's, effectively
    implementing infinite scroll for a series of tables of slots.
    '''

    requested_next = pyqtSignal(datetime.date)
    requested_prev = pyqtSignal(datetime.date)

    requested_date = pyqtSignal(datetime.date)
    requested_dates = pyqtSignal(datetime.date, datetime.date)

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        self.widgets = {}
        self.space_above = 0
        self.space_below = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    @pyqtSlot(list)
    def show(self, models):
        for model in models:
            view = TTableView(self)

            view.setModel(model)

            self.layout.addWidget(view)

    @pyqtSlot(LoadFailed)
    def fail(self, reason: LoadFailed):
        pass


class TScrollArea(QScrollArea):
    '''
    Provide the top-level scroll-enabled area
    '''

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.widget = TScrollWidget(parent=self)

        self.setWidget(self.widget)
        self.setWidgetResizable(True)

    def event(self, event: QEvent):

        if isinstance(event, QResizeEvent):
            self.logger.info(f'ScrollArea ResizeEvent {event.oldSize()} -> {event.size()}')
        elif isinstance(event, QMoveEvent):
            self.logger.info(f'ScrollArea MoveEvent {event.oldPos()} -> {event.pos()}')
        else:
            self.logger.info(f'ScrollArea {event}')

        return super().event(event)
