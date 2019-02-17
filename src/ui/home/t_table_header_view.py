import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.common.logger import logged


class THeaderView(QHeaderView):
    """
    Control size/resize of headers for the SlotTableView

    Note:
        There is trouble if .setModel is called at the wrong moment, more here:
        https://stackoverflow.com/q/48361795/1269892
    """

    def __init__(
        self
        , orientation: Qt.Orientation=Qt.Horizontal
        , parent     : QWidget=None
    ) -> None:
        super().__init__(orientation, parent)

        self.logger = logging.getLogger('tslot')

        self.section_resize_modes = [
            QHeaderView.Stretch # name of task
            , QHeaderView.Stretch # list of tags
            , QHeaderView.ResizeToContents # start time
            , QHeaderView.ResizeToContents # finish time
            , QHeaderView.ResizeToContents # elapsed time
            , QHeaderView.ResizeToContents # nuke button
        ]

        self.hide()

    @logged(disabled=True)
    def setModel(self, model: QAbstractItemModel=None):
        """
        Set the underlying data model

        Fine-grained resizing of individual sections requires calling
        setSectionResizeMode which works only when you've set the model.
        """

        if model is None:
            raise RuntimeError('Must provide a model')

        super().setModel(model)

        if self.count() == 0:
            return # if the model is empty, there is nothing to adjust here

        if self.count() != model.columnCount():
            raise RuntimeError('model.columnCount() != self.count()')
        if self.count() != len(self.section_resize_modes):
            raise RuntimeError('self.count() != len(self.section_resize_modes)')

        # The loop below is the only reason why this method has been overridden
        for i, mode in enumerate(self.section_resize_modes):
            self.setSectionResizeMode(i, mode)

    @logged(logger=logging.getLogger("tslot-main"), disabled=True)
    def sectionSizeHint(self, logical_index: int) -> int:

        return super().sectionSizeHint(logical_index)

    @logged(logger=logging.getLogger("tslot-main"), disabled=True)
    def minimumSectionSize(self) -> int:

        return super().minimumSectionSize()

    @logged(logger=logging.getLogger("tslot-main"), disabled=True)
    def maximumSectionSize(self) -> int:

        return super().maximumSectionSize()
