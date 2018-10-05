import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.utils import item_flags_as_str, logged, pendulum2str, timedelta2str


class TTableModel(QAbstractTableModel):

    def __init__(self, items: list, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        self.items = items

    def rowCount(self, parent: QModelIndex=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent: QModelIndex=QModelIndex()):
        return 6

    @logged(disabled=False)
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:

        return Qt.ItemIsEnabled | Qt.ItemIsEditable

        # flags = super().flags(index)
        #
        # self.logger.debug(f'flags: {item_flags_as_str(flags)}')
        #
        # return flags

    def headerData(
        self
        , section    : int
        , orientation: Qt.Orientation
        , role       : Qt.ItemDataRole=Qt.DisplayRole
    ) -> QVariant:

        if orientation == Qt.Vertical:
            return super().headerData(section, orientation, role)

        if role == Qt.DisplayRole:
            return self.headerDataDisplayRole(section)

        return super().headerData(section, orientation, role)

    def headerDataDisplayRole(self, section: int) -> QVariant:
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
        elif section == 5:
            return 'Nuke button'

        raise RuntimeError(f'Fix .headerDataDisplayRole: section {section}')

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

        return QVariant()

    def dataDisplayRole(self, index: QModelIndex=QModelIndex()):

        row, column = index.row(), index.column()

        slot, task, tags = self.items[row]

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

        return QVariant()

    def dataTextAlignmentRole(self, index: QModelIndex=QModelIndex()):

        if index.column() in [2, 3, 4]:
            return Qt.AlignCenter

        return QVariant()
