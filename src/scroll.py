import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.msg.base import TRequest, TResponse, TFailure
from src.msg.fetch_slot import TRaySlotFetchRequest, TRaySlotFetchResponse
from src.slot import TTableModel, TTableView
from src.utils import logged


class TScrollWidget(QWidget):
    '''
    Provide the top-level widget for the scroll-enabled area

    This widget should add/remove incoming SlotTableView's, effectively
    implementing infinite scroll for a series of tables of slots.
    '''

    requested = pyqtSignal(TRequest)

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

        self.widgets = {}
        self.space_above = 0
        self.space_below = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def kickstart(self):
        self.requested.emit(TRaySlotFetchRequest(slice_lst=3))

    @pyqtSlot(TResponse)
    def handle_responded(self, response: TResponse):

        if isinstance(response, TRaySlotFetchResponse):

            self.handle_responded0(response)

        self.logger.info(f'{self.name} skips {type(response)}')

    def handle_responded0(self, response: TRaySlotFetchResponse):

        pass

    @pyqtSlot(TFailure)
    def handle_triggered(self, failure: TFailure):
        raise NotImplementedError("TScrollWidget.handle_triggered")


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
