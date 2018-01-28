import logging

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.broker import DataBroker
from src.slot import TTableModel, TTableView
from src.utils import logged


class TScrollWidget(QWidget):
    '''
    Provide the top-level widget for the scroll-enabled area

    This widget should add/remove incoming SlotTableView's, effectively
    implementing infinite scroll for a series of tables of slots.
    '''

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.broker = DataBroker(parent=self)

        self.tables = []

        self.slice_fst = 0
        self.slice_lst = 100
        self.slice_dst = 100

        self.load_slots()

    @logged
    def load_slots(self):
        '''
        Attempt to load slots (if there are any)
        '''

        self.broker.load_slots(
            fn_loaded=self.fn_loaded
            , slice_fst=self.slice_fst
            , slice_lst=self.slice_lst
        )

        self.views = []
        self.models = []

        self.slice_fst = self.slice_lst
        self.slice_lst += self.slice_dst

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

            view = TTableView()
            view.setModel(model)

            self.views.append(view)
            self.models.append(model)

            self.layout.addWidget(view)

            lft = rgt

    @logged
    def find_next_lft(self, lft, entries):
        _, _, lslot = entries[lft]

        for rgt, entry in enumerate(entries[lft:], lft):
            _, _, rslot = entry

            if lslot.fst.date() != rslot.fst.date():
                return rgt

        return len(entries)


class TScrollArea(QScrollArea):
    '''
    Provide the top-level scroll-enabled area
    '''

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        self.main_widget = TScrollWidget(self)

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)
