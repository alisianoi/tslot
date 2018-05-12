import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.ui.home.t_table_header_view import THeaderView


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
