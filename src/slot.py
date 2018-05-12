import logging

from datetime import datetime
from operator import itemgetter

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.utils import logged
from src.utils import orient2str, role2str
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


class THeaderView(QHeaderView):
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

        Stretch = QHeaderView.Stretch
        ResizeToContents = QHeaderView.ResizeToContents

        self.section_resize_modes = [
            Stretch # name of task
            , Stretch # list of tags
            , ResizeToContents # start time
            , ResizeToContents # finish time
            , ResizeToContents # elapsed time
        ]

    @logged
    def setModel(self, model: QAbstractItemModel=None):
        '''
        Set the underlying data model

        Fine-grained resizing of individual sections requires calling
        setSectionResizeMode which works only when you've set the model.
        '''
        if model is None:
            raise RuntimeError('Must provide a model')

        super().setModel(model)

        if model.columnCount() != self.count():
            raise RuntimeError('model.columnCount() != self.count()')

        # The loop below is the only reason why this method exists
        for i, mode in enumerate(self.section_resize_modes):
            self.setSectionResizeMode(i, mode)


class TTableView(QTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        self.verticalHeader().hide()

        # Horizontal size can grow/shrink as parent widget sees fit
        # Vertical size must be at least the size of vertical size hint
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        # Since we're demanding that all vertical size be allocated to
        # the table view, let's disable the vertical scrollbar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setFont(QFont('Quicksand-Medium', 12))

        self.setShowGrid(False)
        self.setAlternatingRowColors(True)

    def sizeHint(self):

        model = self.model()

        # self.logger.info(model)

        if model is None:
            return super().sizeHint()

        height = self.horizontalHeader().height()
        for i in range(model.rowCount()):
            height += self.rowHeight(i)

        return QSize(super().sizeHint().width(), height)

    def setModel(self, model: QAbstractItemModel):

        super().setModel(model)

        # The code below is the reason why this method is overwritten
        # It creates a brand new header view, installs and triggers it
        self.header_view = THeaderView(
            orientation=Qt.Horizontal, parent=self
        )

        self.setHorizontalHeader(self.header_view)

        self.header_view.setModel(model)
