import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.common.logger import logged, logmain
from src.utils import style_option_as_str


class THomeTableStyleDelegate(QStyledItemDelegate):
    """Draw a push button instead of a table cell."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @logged(logger=logging.getLogger("tslot-main"), disabled=True)
    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget:

        if index.column() not in [0, 1, 2, 3]:
            raise RuntimeError(f'Editor for column {index.column()}')

        # alternative: return QLineEdit(parent)
        return super().createEditor(parent, option, index)

    @logged(disabled=False)
    def setEditorData(self, editor: QWidget, index: QModelIndex):

        editor.setText(index.data())

    @logged(disabled=False)
    def setModelData(
        self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex
    ):

        if not isinstance(editor, QLineEdit):
            raise RuntimeError('Expected editor to be QLineEdit')

        model.setData(index, editor.text())

    @logged(disabled=True)
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):

        logmain.debug(f'paint: {index}')

        if index.column() != 5:
            return super().paint(painter, option, index)

        painter.save()

        so_button = QStyleOptionButton()
        so_button.rect = QRect(option.rect)
        so_button.text = 'trash'
        so_button.state = QStyle.State_Enabled

        QApplication.style().drawControl(QStyle.CE_PushButton, so_button, painter)

        painter.restore()

    @logged(logger=logging.getLogger('tslot-main'), disabled=True)
    def sizeHint(self, item: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        size = super().sizeHint(item, index)

        logmain.debug(style_option_as_str(item.type))
        logmain.debug(f'row: {item.index.row()}, col: {item.index.column()}')
        logmain.debug(f'{index.data()}')
        logmain.debug(item.text)

        if index in [2, 3, 4]:
            return size

        # TODO: +20 is the spacing between columns 2, 3 and 4
        return QSize(size.width() + 20, size.height())
