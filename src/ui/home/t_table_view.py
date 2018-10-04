import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QStyleOptionButton

from src.ui.base import TTableView
from src.ui.home.t_table_header_view import THeaderView
from src.utils import logged, style_option_as_str


class TNukeStyleDelegate(QStyledItemDelegate):
    """Draw a push button instead of a table cell."""

    def __init__(self, parent: QWidget=None) -> None:

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

    @logged(disabled=False)
    def createEditor(
        self
        , parent: QWidget
        , option: QStyleOptionViewItem
        , index: QModelIndex
    ) -> QWidget:

        editor = QPushButton(parent)

        editor.setText('trash')

        return editor

    @logged(disabled=True)
    def paint(
        self
        , painter: QPainter
        , option : QStyleOptionViewItem
        , index  : QModelIndex
    ) -> None:

        self.logger.debug(f'paint: {index}')

        if index.column() != 5:
            return super().paint(painter, option, index)

        painter.save()

        so_button = QStyleOptionButton()
        so_button.rect = QRect(option.rect)
        so_button.text = 'trash'
        so_button.state = QStyle.State_Enabled

        QApplication.style().drawControl(QStyle.CE_PushButton, so_button, painter)

        painter.restore()

    @logged(disabled=False)
    def sizeHint(self, item: QStyleOptionViewItem, index: QModelIndex) -> QSize:

        size = super().sizeHint(item, index)

        self.logger.debug(style_option_as_str(item.type))
        self.logger.debug(f'row: {item.index.row()}, col: {item.index.column()}')
        self.logger.debug(f'{index.data()}')
        self.logger.debug(item.text)

        if index in [2, 3, 4]:
            return size

        return QSize(size.width() + 20, size.height())

        # self.logger.debug(f'column: {index.column()}')

        # return super().sizeHint(item, index)


class THomeTableView(TTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.delegate = TNukeStyleDelegate()
        self.setItemDelegate(self.delegate)

        self.verticalHeader().hide()
        self.horizontalHeader().hide()

        # Horizontal size can grow/shrink as parent widget sees fit
        # Vertical size must be at least the size of vertical size hint
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        # Since we're demanding that all vertical size be allocated to
        # the table view, let's disable the vertical scrollbar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setShowGrid(False)
        self.setAlternatingRowColors(True)

    @logged(disabled=True)
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

        self.logger.debug(f'{event.oldSize()} -> {event.size()}')

    @logged(disabled=True)
    def sizeHint(self):
        """Compute the exact required size for the table"""

        size_hint = super().sizeHint()

        h, w = 0, size_hint.width()

        vheader = self.verticalHeader()
        hheader = self.horizontalHeader()

        if not vheader.isHidden():
            self.logger.warning('Expecting vertical header to be hidden')
        if not hheader.isHidden():
            h += hheader.height()

        for i in range(vheader.count()):
            if not vheader.isSectionHidden(i):
                h += vheader.sectionSize(i)

        return QSize(w, h)

    @logged(disabled=True)
    def minimumSizeHint(self):
        return self.sizeHint()

    @logged(disabled=True)
    def setModel(self, model: QAbstractItemModel):

        super().setModel(model)

        # The code below is the reason why this method is overwritten
        # It creates a brand new header view, installs and triggers it
        self.header_view = THeaderView(Qt.Horizontal, self)

        self.setHorizontalHeader(self.header_view)

    @logged(disabled=False)
    def enterEvent(self, event: QEvent) -> None:

        super().enterEvent(event)

    @logged(disabled=False)
    def leaveEvent(self, event: QEvent) -> None:

        super().leaveEvent(event)
