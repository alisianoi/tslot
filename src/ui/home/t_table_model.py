import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.utils import logged
from src.utils import pendulum2str, timedelta2str


class TTableModel(QAbstractTableModel):

    def __init__(self, items: list, parent: QObject=None):

        super().__init__(parent)

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

        self.entries = items

    @logged
    def headerData(
        self
        , section    : int
        , orientation: Qt.Orientation
        , role       : Qt.ItemDataRole=Qt.DisplayRole
    ):

        if orientation == Qt.Vertical:
            return super().headerData(section, orientation, role)

        if role == Qt.DisplayRole:
            return self.headerDataDisplayRole(section)

        return super().headerData(section, orientation, role)

    @logged
    def headerDataDisplayRole(self, section: int):
        if section == 0:
            return 'Task'
        elif section == 1:
            return 'Tag'
        elif section == 2:
            return 'Started'
        elif section == 3:
            return 'Stopped'
        elif section == 4:
            return 'Elapsed'

        return 'Fix Header'

    def rowCount(self, parent: QModelIndex=QModelIndex()):
        return len(self.entries)

    def columnCount(self, parent: QModelIndex=QModelIndex()):
        return 5

    @logged
    def data(
        self
        , index: QModelIndex=QModelIndex()
        , role : Qt.ItemDataRole=Qt.DisplayRole
    ):

        if not index.isValid():
            self.logger.debug('Requested index is not valid')
            return QVariant()

        if not 0 <= index.row() < self.rowCount():
            self.logger.debug('Requested row is outside range')
            return QVariant()

        if not 0 <= index.column() <= self.columnCount():
            self.logger.debug('Requested column is outside range')
            return QVariant()

        if role == Qt.DisplayRole:
            return self.dataDisplayRole(index)

        if role == Qt.TextAlignmentRole:
            return self.dataTextAlignmentRole(index)

        self.logger.debug('Defaulting to QVariant')
        return QVariant()

    def dataDisplayRole(self, index: QModelIndex=QModelIndex()):

        row, column = index.row(), index.column()

        slot, task, tags = self.entries[row]

        if column == 0:
            return task.name

        if column == 1:
            return ' '.join(tag.name for tag in tags)

        if column == 2:
            return pendulum2str(slot.fst)

        if column == 3:
            return pendulum2str(slot.lst)

        if column == 4:
            return timedelta2str(slot.lst - slot.fst)

        self.logger.debug('Defaulting to QVariant')
        return QVariant()

    def dataTextAlignmentRole(self, index: QModelIndex=QModelIndex()):

        if index.column() == 4:
            return Qt.AlignVCenter | Qt.AlignRight

        self.logger.debug('Defaulting to QVariant')
        return QVariant()