import logging

from datetime import date, datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.db.broker import DataBroker
from src.slot import TTableModel, TTableView
from src.utils import logged


class TScrollCache(QObject):

    loaded_next = pyqtSignal(TTableModel)
    loaded_prev = pyqtSignal(TTableModel)

    loaded_date = pyqtSignal(TTableModel)
    loaded_dates = pyqtSignal(list)

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        self.models = []
        self.model_index = 0

        self.slice_fst = 0
        self.slice_lst = 100

        self.broker = DataBroker(self)

    @pyqtSlot()
    def load_next(self):

        if self.model_index < len(self.models):
            self.loaded_next.emit(self.models[self.model_index])

            self.model_index += 1

    def load_prev(self):
        pass

    def load_date(self, date: date):
        pass

    def load_dates(self, fst_date: date, lst_date: date):
        pass

    def load_slots(self):

        self.broker.load_slots(
              fn_loaded=self.fn_loaded
            , slice_fst=self.slice_fst
            , slice_lst=self.slice_lst
        )

    @logged
    @pyqtSlot(list)
    def fn_loaded(self, entries):
        lft = 0

        while lft != len(entries):
            rgt = self.find_next_lft(lft, entries)

            # All slots in [lft, rgt) belong to the nsame date, so they
            # must end up in the same model of the same table view

            model = TTableModel()

            model.beginInsertRows(QModelIndex(), lft, rgt)
            model.entries[lft:rgt] = entries[lft:rgt]
            model.endInsertRows()

            self.models.append(model)

            lft = rgt

    @logged
    def find_next_lft(self, lft, entries):
        _, _, lslot = entries[lft]

        for rgt, entry in enumerate(entries[lft:], lft):
            _, _, rslot = entry

            if lslot.fst.date() != rslot.fst.date():
                return rgt

        return len(entries)


class TScrollWidget(QWidget):
    '''
    Provide the top-level widget for the scroll-enabled area

    This widget should add/remove incoming SlotTableView's, effectively
    implementing infinite scroll for a series of tables of slots.
    '''

    requested_next = pyqtSignal()
    requested_prev = pyqtSignal()

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        self.widgets = {}
        self.space_above = 0
        self.space_below = 0

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.request_next()

    @pyqtSlot()
    def request_next(self):
        '''
        Request more data for widgets

        Stop once there is no more data or screen space if full
        '''

        self.logger.info('TScrollWidget reports:')
        self.logger.info(f'Position: {self.pos()}')

        point = self.pos()
        self.logger.info(f'Coordinates: {point.x(), point.y()}')

        self.logger.info(f'Height: {self.height()}')
        if self.height() == 0 or self.space_below < self.height():
            self.requested_next.emit()

    @pyqtSlot()
    def display_next(self):
        pass

    def event(self, event: QEvent):

        if isinstance(event, QWheelEvent):
            self.logger.info(f'ScrollWidget QWheelEvent {event.pixelDelta()}px')
            self.request_next()

        return super().event(event)



class TScrollArea(QScrollArea):
    '''
    Provide the top-level scroll-enabled area
    '''

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_cache = TScrollCache(parent=self)
        self.scroll_widget = TScrollWidget(parent=self)

        self.scroll_widget.requested_next.connect(
            self.scroll_cache.load_next
        )
        self.scroll_widget.requested_prev.connect(
            self.scroll_cache.load_prev
        )

        self.setWidget(self.scroll_widget)
        self.setWidgetResizable(True)

    def event(self, event: QEvent):

        if isinstance(event, QResizeEvent):
            self.logger.info(f'ScrollArea ResizeEvent {event.oldSize()} -> {event.size()}')
        elif isinstance(event, QMoveEvent):
            self.logger.info(f'ScrollArea MoveEvent {event.oldPos()} -> {event.pos()}')
        else:
            self.logger.info(f'ScrollArea {event}')

        return super().event(event)
