import logging

from operator import itemgetter

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TSlotTableModel(QAbstractTableModel):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

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
            return 'Tag'
        elif section == 2:
            return 'Started'
        else:
            return 'Stopped'

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

        if not 0 <= row < len(self.entries):
            self.logger.debug('Requested row is outside range')

            return QVariant()

        tag, task, slot = self.entries[row]

        if column == 0:
            return task.name

        if column == 1:
            return tag.name

        if column == 2:
            return slot.fst

        if column == 3:
            return slot.lst

    def setData(
            self
            , index: QModelIndex
            , value: QVariant
            , role : Qt.ItemDataRole=Qt.EditRole
    ):
        self.logger.debug('enter .setData:')
        self.logger.debug('index: {}'.format(index))
        self.logger.debug('value: {}'.format(value))
        self.logger.debug('role : {}'.format(role))

        return (False, self.logger.debug('leave (False)'))[0]

    def insertRow(self, row: int, parent: QModelIndex=QModelIndex()):
        self.logger.debug('enter .insertRow')
        self.logger.debug('row   : {}'.format(row))
        self.logger.debug('parent: {}'.format(parent))

        return (False, self.logger.debug('leave (False)'))[0]

    def insertRows(
            self
            , row   : int
            , count : int
            , parent: QModelIndex=QModelIndex()
    ):
        self.logger.debug('enter .insertRows')
        self.logger.debug('row   : {}'.format(row))
        self.logger.debug('count : {}'.format(count))
        self.logger.debug('parent: {}'.format(parent))

        if 0 <= row <= self.rowCount():
            self.beginInsertRows(parent, row, row + count)

            return True, self.logger.debug('leave (True)')

        return False, self.logger.debug('leave (False)')

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

        self.logger.debug('enter .find_lft_index')
        self.logger.debug('entry  : {}'.format(entry))
        self.logger.debug('entries: {}'.format(entries))
        self.logger.debug('key    : {}'.format(key))

        slot0 = key(entry)
        lo, hi = 0, len(entries) - 1

        while lo <= hi:
            mid = lo + (hi - lo) // 2

            slot1 = key(entries[mid])

            if slot0 <= slot1:
                hi = mid - 1
            else:
                lo = mid + 1

        self.logger.debug('leave {}'.format(lo))

        return lo

    @pyqtSlot(list)
    def fn_loaded(self, entries):
        '''
        Responds to the loaded signal of the DataBroker.

        Should traverse the list of entries and add them to the ones
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

    @pyqtSlot()
    def fn_started(self):
        self.logger.debug('handle_started')

    @pyqtSlot()
    def fn_stopped(self):
        self.logger.debug('handle_stopped')


class TSlotTableView(QTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)
