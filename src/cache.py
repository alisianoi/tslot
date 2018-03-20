import datetime
import logging

from PyQt5.QtCore import *

from src.scroll import TTableModel
from src.db.loader import LoadFailed


class TDataCache(QObject):

    requested_next = pyqtSignal(datetime.date)
    requested_prev = pyqtSignal(datetime.date)

    requested_date = pyqtSignal(datetime.date)
    requested_dates = pyqtSignal(datetime.date, datetime.date)

    loaded = pyqtSignal(list)
    failed = pyqtSignal(LoadFailed)

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

    @pyqtSlot(datetime.date)
    def load_next(self, date: datetime.date):
        # TODO: add cache manipulations here
        self.requested_next.emit(date)

    @pyqtSlot(datetime.date)
    def load_prev(self, date: datetime.date):
        # TODO: add cache manipulations here
        self.reqeusted_prev.emit(date)

    @pyqtSlot(datetime.date)
    def load_date(self, date: datetime.date):
        # TODO: add cache manipulations here
        self.requested_date.emit(date)

    @pyqtSlot(datetime.date, datetime.date)
    def load_dates(self, fst_date: datetime.date, lst_date: datetime.date):
        # TODO: add cache manipulations here
        self.requested_dates.emit(fst_date, lst_date)

    @pyqtSlot(list)
    def cache(self, entries):
        if not entries:
            return self.loaded.emit([])

        models = []
        fst, lst, n = 0, 0, len(entries)

        while fst != n:

            model = TTableModel()

            while lst != n and entries[fst][0] == entries[lst][0]:

                model.entries.append(entries[lst])

                lst += 1

            models.append(model)

            fst = lst

        self.loaded.emit(models)
