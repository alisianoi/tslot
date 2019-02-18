import logging

from PyQt5.QtCore import QAbstractItemModel, Qt
from PyQt5.QtWidgets import QSizePolicy

from src.client.common.widget.table_view import TTableView
from src.client.wgt_timer_table.widget.header_view import THeaderView
from src.client.wgt_timer_table.widget.styled_item_delegate import *
from src.common.logger import logged


class THomeTableView(TTableView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.delegate = THomeTableStyleDelegate()
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

    @logged(logger=logging.getLogger('tslot-main'), disabled=True)
    def sizeHint(self):
        """Compute the exact required size for the table"""

        size_hint = super().sizeHint()

        h, w = 0, size_hint.width()

        vheader = self.verticalHeader()
        hheader = self.horizontalHeader()

        if not vheader.isHidden():
            logmain.warning('Expecting vertical header to be hidden')
        if not hheader.isHidden():
            h += hheader.height()

        for i in range(vheader.count()):
            if not vheader.isSectionHidden(i):
                h += vheader.sectionSize(i)

        return QSize(w, h)

    @logged(logger=logging.getLogger('tslot-main'), disabled=True)
    def minimumSizeHint(self):
        return self.sizeHint()

    @logged(logger=logging.getLogger('tslot-main'), disabled=True)
    def setModel(self, model: QAbstractItemModel):

        super().setModel(model)

        # The code below is the reason why this method is overwritten
        # It creates a brand new header view, installs and triggers it
        self.header_view = THeaderView(orientation=Qt.Horizontal, parent=self)

        self.setHorizontalHeader(self.header_view)
