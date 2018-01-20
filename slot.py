import logging

from datetime import datetime
from operator import itemgetter

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from model import Tag, Task, Slot


def orient2str(orientation: Qt.Orientation):
    if orientation == 0x1 and orientation == Qt.Horizontal:
        return 'Qt.Horizontal'
    elif orientation == 0x2 and orientation == Qt.Vertical:
        return 'Qt.Vertical'

    return 'Unknown Orientation (Orientation Number Change?): ' + str(orientation)

def role2str(role: Qt.ItemDataRole):
    if role == 0 and role == Qt.DisplayRole:
        return 'Qt.DisplayRole'
    elif role == 1 and role == Qt.DecorationRole:
        return 'Qt.DecorationRole'
    elif role == 2 and role == Qt.EditRole:
        return 'Qt.EditRole'
    elif role == 3 and role == Qt.ToolTipRole:
        return 'Qt.ToolTipRole'
    elif role == 4 and role == Qt.StatusTipRole:
        return 'Qt.StatusTipRole'
    elif role == 5 and role == Qt.WhatsThisRole:
        return 'Qt.WhatsThisRole'
    elif role == 6 and role == Qt.FontRole:
        return 'Qt.FontRole'
    elif role == 7 and role == Qt.TextAlignmentRole:
        return 'Qt.TextAlignmentRole'
    elif role == 8 and role == Qt.BackgroundRole:
        return 'Qt.BackgroundRole'
    elif role == 9 and role == Qt.ForegroundRole:
        return 'Qt.ForegroundRole'
    elif role == 10 and role == Qt.CheckStateRole:
        return 'Qt.CheckStateRole'
    elif role == 11 and role == Qt.AccessibleTextRole:
        return 'Qt.AccessibleTextRole'
    elif role == 12 and role == Qt.AccessibleDescriptionRole:
        return 'Qt.AccessibleDescriptionRole'
    elif role == 13 and role == Qt.SizeHintRole:
        return 'Qt.SizeHintRole'
    elif role == 14 and role == Qt.InitialSortOrderRole:
        return 'Qt.InitialSortOrderRole'
    elif role == 32 and role == Qt.UserRole:
        return 'Qt.UserRole'

    return 'Unknown Role (Role Number Change?): ' + str(role)


class TSlotTableModel(QAbstractTableModel):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug('TSlotTableModel has a logger')

        self.entries = [(
            Tag(name='whatever')
            , Task(name='what what?')
            , Slot(fst=datetime.utcnow(), lst=datetime.utcnow())   
        )]

    def headerData(
        self
        , section    : int
        , orientation: Qt.Orientation
        , role       : Qt.ItemDataRole=Qt.DisplayRole
    ):
        self.logger.debug('enter .headerData')
        self.logger.debug('section    : {}'.format(section))
        self.logger.debug('orientation: {}'.format(orient2str(orientation)))
        self.logger.debug('role       : {}'.format(role2str(role)))

        if orientation == Qt.Vertical:
            self.logger.debug('leave (Qt.Vertical, ask parent)')

            return super().headerData(section, orientation, role)
        if role == Qt.DisplayRole:
            self.logger.debug('leave (Qt.DisplayRole)')

            return self.headerDataDisplayRole(section)

        self.logger.debug('leave (Fallthrough, ask parent)')
        return super().headerData(section, orientation, role)

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

    def data(
        self
        , index: QModelIndex=QModelIndex()
        , role : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if role != Qt.DisplayRole:
            return QVariant()

        row, column = index.row(), index.column()

        if not 0 <= row < self.rowCount():
            self.logger.debug('Requested row is outside range')

            return QVariant()

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

            return (True, self.logger.debug('leave (True)'))[0]

        return (False, self.logger.debug('leave (False)'))[0]

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

    @pyqtSlot()
    def fn_started(self):
        self.logger.debug('enter .fn_started')
        self.logger.debug('leave .fn_started')

    @pyqtSlot()
    def fn_stopped(self):
        self.logger.debug('enter .fn_stopped')
        self.logger.debug('leave .fn_stopped')


class TSlotHorizontalHeaderView(QHeaderView):

    def __init__(
            self
            , orientation: Qt.Orientation=Qt.Horizontal
            , parent     : QWidget=None
    ):
        super().__init__(orientation, parent)

        self.logger = logging.getLogger('tslot')

    def sizeHint(self):
        self.logger.debug('enter .sizeHint')
        self.logger.debug('leave ({})'.format(super().sizeHint()))
        return super().sizeHint()

    def sectionSizeHint(self, logicalIndex: int):
        self.logger.debug('enter .sectionSizeHint')
        self.logger.debug('leave (400)')
        return 400

    def sectionSize(self, logicalIndex: int):
        self.logger.debug('enter .sectionSize')
        self.logger.debug('leave (400)')
        return 400

    def defaultSectionSize(self, logicalIndex: int):
        self.logger.debug('enter .defaultSectionSize')
        self.logger.debug('leave (400)')
        return 400

    def minimumSectionSize(self):
        self.logger.debug('enter .minimumSectionSize')
        self.logger.debug('leave ({})'.format(super().minimumSectionSize()))
        return super().minimumSectionSize()

    def resizeMode(self, logicalIndex: int):
        self.logger.debug('enter .resizeMode')
        self.logger.debug('leave (QHeaderView.Fixed)')
        return QHeaderView.Fixed


class TSlotHorizontalHeaderView(QHeaderView):

    def __init__(
        self
        , orientation: Qt.Orientation=Qt.Horizontal
        , parent     : QWidget=None
    ):
        super().__init__(orientation, parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug('TSlotHorizontalHeaderView has a logger')

    def sectionResizeMode(logicalIndex: int) -> QHeaderView.ResizeMode:
        self.logger.debug('enter .sectionResizeMode')
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

        return QHeaderView.Fixed


class TSlotTableView(QTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        # Remove little blank space
        self.verticalHeader().hide()
