import logging
from typing import List

from PyQt5.QtCore import *

from src.ai.model import TEntryModel
from src.common.logger import logged
from src.utils import pendulum2str, timedelta2str


class TTableModel(QAbstractTableModel):

    def __init__(self, items: List[TEntryModel], **kwargs):
        super().__init__(**kwargs)
        self.items = items

    def rowCount(self, parent: QModelIndex=QModelIndex()):
        return len(self.items)

    def columnCount(self, parent: QModelIndex=QModelIndex()):
        return 6

    @logged(logger=logging.getLogger("tslot-main"), disabled=True)
    def flags(self, index: QModelIndex) -> Qt.ItemFlags:

        return Qt.ItemIsEnabled | Qt.ItemIsEditable

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

    @logged(logger=logging.getLogger('tslot-main'), disabled=True)
    def data(
        self, index: QModelIndex=QModelIndex(), role: Qt.ItemDataRole=Qt.DisplayRole
    ):
        if not self.check_index(index):
            raise RuntimeError('data expects an index that makes sense')

        if role == Qt.EditRole:
            return self.dataDisplayRole(index)

        if role == Qt.DisplayRole:
            return self.dataDisplayRole(index)

        if role == Qt.TextAlignmentRole:
            return self.dataTextAlignmentRole(index)

        return QVariant()

    def dataDisplayRole(self, index: QModelIndex=QModelIndex()):

        row, column = index.row(), index.column()

        entry = self.items[row]

        slot, task, tags = entry.slot, entry.task, entry.tags

        if column == 0:
            return task.name
        elif column == 1:
            return ' '.join(tag.name for tag in tags)
        elif column == 2:
            return pendulum2str(slot.fst)
        elif column == 3:
            return pendulum2str(slot.lst)
        elif column == 4:
            return timedelta2str(slot.lst - slot.fst)

        return QVariant()

    def dataTextAlignmentRole(self, index: QModelIndex=QModelIndex()):

        if index.column() in [2, 3, 4]:
            return Qt.AlignCenter

        return QVariant()

    @logged(logger=logging.getLogger('tslot-main'), disabled=False)
    def setData(
        self
        , index: QModelIndex
        , value: QVariant
        , role: int=Qt.EditRole
    ) -> bool:

        if role != Qt.EditRole:
            return super().setData(index, value, role)

        if not self.check_index(index):
            raise RuntimeError('setData expects an index that makes sense')

        if index.column() == 0:
            self.setDataForTask(index, value)
        elif index.column() == 1:
            self.setDataForTag(index, value)
        else:
            raise RuntimeError(f'setData not implemented for {index.column()}')

        self.dataChanged.emit(index, index, [role])

        return True

    @logged(logger=logging.getLogger('tslot-main'), disabled=False)
    def setDataForTask(self, index: QModelIndex, value: QVariant) -> None:

        self.items[index.row()].task.name = value

    @logged(logger=logging.getLogger('tslot-main'), disabled=False)
    def setDataForTag(self, index: QModelIndex, value: QVariant) -> None:

        new_tags, old_tags = [], self.items[index.row()].tags

        for name in value.split(' '):
            for tag in old_tags:
                if tag.name == name:
                    new_tags.append(tag)

                    break
            else:
                # It could be a *completely* new tag or an existing tag that was
                # not used for this task before. Which is it?
                raise RuntimeError('Need a working tag by name search!')

    def check_index(self, index: QModelIndex) -> bool:
        """Check if the supplied index makes sense"""

        if not index.isValid():
            return False

        row = index.row()

        if row < 0 or row >= self.rowCount():
            return False

        column = index.column()

        if column < 0 or column >= self.columnCount():
            return False

        return True
