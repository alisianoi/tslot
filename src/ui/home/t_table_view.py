import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.ui.base import TTableView
from src.ui.home.t_table_header_view import THeaderView
from src.utils import logged


class THomeTableView(TTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        self.verticalHeader().hide()
        self.horizontalHeader().hide()

        # Horizontal size can grow/shrink as parent widget sees fit
        # Vertical size must be at least the size of vertical size hint
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        # Since we're demanding that all vertical size be allocated to
        # the table view, let's disable the vertical scrollbar
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setFont(QFont('Quicksand-Medium', 12))

        # self.setShowGrid(False)
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
