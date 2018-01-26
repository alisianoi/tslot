import logging

from datetime import datetime
from operator import itemgetter

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.model import Tag, Task, Slot
from src.utils import orient2str, role2str, logged


class TSlotTableModel(QAbstractTableModel):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug('TSlotTableModel has a logger')

        self.entries = []

    @logged
    def headerData(
        self
        , section    : int
        , orientation: Qt.Orientation
        , role       : Qt.ItemDataRole=Qt.DisplayRole
    ):
        self.logger.debug('section    : {}'.format(section))
        self.logger.debug('orientation: {}'.format(orient2str(orientation)))
        self.logger.debug('role       : {}'.format(role2str(role)))

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

    # def headerDataSizeHintRole(self, section: int):
    #     self.logger.debug('enter .headerDataSizeHintRole')

    #     return QSize(200, 30)

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

        tag, task, slot = self.entries[row]

        if column == 0:
            return task.name

        if column == 1:
            return tag.name

        if column == 2:
            return str(slot.fst)

        if column == 3:
            return str(slot.lst)

        if column == 4:
            return str(slot.lst - slot.fst)

        self.logger.debug('Defaulting to QVariant')
        return QVariant()

    def dataTextAlignmentRole(self, index: QModelIndex=QModelIndex()):

        if index.column() == 4:
            return Qt.AlignVCenter | Qt.AlignRight

        self.logger.debug('Defaulting to QVariant')
        return QVariant()

    @logged
    def setData(
            self
            , index: QModelIndex
            , value: QVariant
            , role : Qt.ItemDataRole=Qt.EditRole
    ):
        self.logger.debug('enter .setData:')
        self.logger.debug('index: {}'.format(index))
        self.logger.debug('value: {}'.format(value))
        self.logger.debug('role : {}'.format(role2str(role)))

        return False

    @logged
    def insertRow(self, row: int, parent: QModelIndex=QModelIndex()):
        self.logger.debug('row   : {}'.format(row))
        self.logger.debug('parent: {}'.format(parent))

        return False

    @logged
    def insertRows(
            self
            , row   : int
            , count : int
            , parent: QModelIndex=QModelIndex()
    ):
        self.logger.debug('row   : {}'.format(row))
        self.logger.debug('count : {}'.format(count))
        self.logger.debug('parent: {}'.format(parent))

        if 0 <= row <= self.rowCount():
            self.beginInsertRows(parent, row, row + count)

            return True

        return False

    @logged
    def find_lft_index(self, entry, entries, key=itemgetter(2)):
        '''
        Find the *very first* entry which is >= the given entry.

        This gives the leftmost index at which it would be possible to
        insert the given entry and maintain the list in sorted order.

        Args:
            entry  : the potentially new entry
            entries: the list of existing entries
            key    : the standard key function, see [1]

        Returns:
            An index from [0, len(entries)] suitable for insertion

        [1] https://docs.python.org/3/howto/sorting.html#key-functions
        '''

        slot0 = key(entry)
        lo, hi = 0, len(entries) - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2

            slot1 = key(entries[mid])

            if slot0 <= slot1:
                hi = mid - 1
            else:
                lo = mid + 1

        return lo

    @pyqtSlot(list)
    def fn_loaded(self, entries):
        '''
        Responds to the loaded signal of the DataBroker.

        Traverse the received list of entries and add them to the ones
        already stored in memory by this model.

        Args:
            entries: a list of (tag, task, slot) from the database
        '''

        for entry in entries:
            row = self.find_lft_index(entry, self.entries)

            if row != len(self.entries) and entry == self.entries[row]:
                self.logger.debug('There are two identical entries:')
                self.logger.debug('{}, {}, {}'.format(*entry))
                self.logger.debug('{}, {}, {}'.format(*self.entries[row]))
                self.logger.debug('Will not change entry ' + str(row))

                continue

            self.logger.debug('About to add entry at index ' + str(row))
            self.logger.debug('{}, {}, {}'.format(*entry))

            self.beginInsertRows(QModelIndex(), row, row)

            self.entries.insert(row, entry)

            self.endInsertRows()

    @logged
    @pyqtSlot()
    def fn_started(self):
        pass

    @logged
    @pyqtSlot()
    def fn_stopped(self):
        pass


class TSlotHorizontalHeaderView(QHeaderView):
    '''
    Control size/resize of headers for the SlotTableView

    Note:
        https://stackoverflow.com/q/48361795/1269892
    '''

    def __init__(
            self
            , orientation: Qt.Orientation=Qt.Horizontal
            , parent     : QWidget=None
    ):
        super().__init__(orientation, parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug('TSlotHorizontalHeaderView has a logger')

        Stretch, Fixed = QHeaderView.Stretch, QHeaderView.Fixed

        self.section_resize_modes = [
            Stretch, Stretch, Fixed, Fixed, Fixed
        ]

    @logged
    def setModel(self, model: QAbstractItemModel=None):
        '''
        Set the underlying data model

        Fine-grained resizing of individual sections requires calling
        setSectionResizeMode which works only when you've set the model.
        '''
        if model is None:
            raise RuntimeError('model must be not None')

        if model.columnCount() != self.count():
            raise RuntimeError('model.columnCount() != self.count()')

        super().setModel(model)

        # The loop below is the only reason why this method exists
        for i, mode in enumerate(self.section_resize_modes):
            self.setSectionResizeMode(i, mode)

    @logged
    def count(self):
        return len(self.section_resize_modes)

    @logged
    def offset(self):
        return super().offset()

    @logged
    def horizontalOffset(self):
        return super().horizontalOffset()

    @logged
    def verticalOffset(self):
        return super().verticalOffset()

    @logged
    def length(self):
        return super().length()

    @logged
    def sizeHint(self):
        return super().sizeHint()

    @logged
    def sectionSizeHint(self, logicalIndex: int):
        return 400

    @logged
    def sectionSize(self, logicalIndex: int):
        return 400

    @logged
    def defaultSectionSize(self, logicalIndex: int):
        return 400

    @logged
    def minimumSectionSize(self):
        return super().minimumSectionSize()

    @logged
    def resizeMode(self, logicalIndex: int):
        return QHeaderView.Fixed

    @logged
    def sectionResizeMode(logicalIndex: int) -> QHeaderView.ResizeMode:
        if logicalIndex == 0:
            return QHeaderView.Stretch
        if logicalIndex == 1:
            return QHeaderView.Stretch
        if logicalIndex == 2:
            return QHeaderView.Fixed
        if logicalIndex == 3:
            return QHeaderView.Fixed
        if logicalIndex == 4:
            return QHeaderView.Fixed

        self.logger.debug('Defaulting to:')
        return QHeaderView.Fixed

    @logged
    def resizeSection(self, logicalIndex: int, size: int):
        return super().resizeSection(logicalIndex, size)

    @logged
    def stretchSectionCount(self) -> int:
        return super().stretchSectionCount()


class TSlotTableView(QTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        # Remove little blank space
        self.verticalHeader().hide()
