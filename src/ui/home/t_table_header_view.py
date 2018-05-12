import logging

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.utils import logged


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
