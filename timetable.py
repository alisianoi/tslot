import logging

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TrTimeTableModel(QAbstractTableModel):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.entries = []

    def headerData(
            self
            , section: int
            , orientation: Qt.Orientation
            , role=Qt.DisplayRole
    ):

        if role != Qt.DisplayRole:
            return QVariant()

        if section == 0:
            return 'Task'
        elif section == 1:
            return 'Start'
        elif section == 2:
            return 'Stop'
        else:
            return 'Elapsed'

    def rowCount(self, parent: QModelIndex=QModelIndex()):
        return len(self.entries)

    def columnCount(self, parent: QModelIndex=QModelIndex()):
        return 4

    def data(
        self
        , index: QModelIndex=QModelIndex()
        , role=Qt.DisplayRole
    ):
        if role != Qt.DisplayRole:
            return QVariant()

        row, column = index.row(), index.column()


class TrTimeTableView(QTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)
