#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyTableModel(QAbstractTableModel):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.entries = [
              ['row0, col0 (expanding)', 'row0, col1 (expanding)', 'row0, col2']
            , ['row1, col0 (expanding)', 'row1, col1 (expanding)', 'row1, col2']
            , ['row2, col0 (expanding)', 'row2, col1 (expanding)', 'row2, col2']
        ]

    def headerData(
        self
        , section    : int
        , orientation: Qt.Orientation
        , role       : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if orientation == Qt.Vertical:
            return QVariant()

        if role == Qt.DisplayRole:
            if section == 0:
                return 'Expanding 0'
            if section == 1:
                return 'Expanding 1'
            if section == 2:
                return 'Fixed 0'

            return 'Fix Your Columns'

    def data(
        self
        , index: QModelIndex=QModelIndex()
        , role : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if role != Qt.DisplayRole:
            return QVariant()

        return self.entries[index.row()][index.column()]
        
    def rowCount(self, parent: QModelIndex=QModelIndex()):
        return len(self.entries)

    def columnCount(self, parent: QModelIndex=QModelIndex()):
        return len(self.entries[0])


class MyTableView(QTableView):

    def __init__(self, parent: QObject=None):
        super().__init__(parent)


class MyHeaderView(QHeaderView):

    def __init__(
        self
        , orientation: Qt.Orientation=Qt.Horizontal
        , parent     : QWidget=None
    ):
        super().__init__(orientation, parent)

        Stretch, Fixed = QHeaderView.Stretch, QHeaderView.Fixed
        self.SECTION_RESIZE_MODES = [Stretch, Stretch, Fixed]

    def column(self) -> int:
        return 3

    def setModel(self, model: QAbstractItemModel=None):

        super().setModel(model)

        for i, mode in enumerate(self.SECTION_RESIZE_MODES):
            print(i, mode)
            self.setSectionResizeMode(i, mode)


class MyCentralWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.my_table_model = MyTableModel(parent=parent)

        self.my_table_view = MyTableView(parent=parent)
        self.my_header_view = MyHeaderView(parent=parent)

        self.my_table_view.setModel(self.my_table_model)
        self.my_header_view.setModel(self.my_table_model)

        self.my_table_view.setHorizontalHeader(self.my_header_view)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.my_table_view)

        self.setLayout(self.layout)


class MyMainWindow(QMainWindow):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.central_widget = MyCentralWidget(self)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())
