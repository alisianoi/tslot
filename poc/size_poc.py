#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyPushButton(QPushButton):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.setText('Hello, world!')

        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)

    def sizeHint(self):
        return QSize(300, 300)


class MyTableModel(QAbstractTableModel):

    def __init__(self, i: int, parent: QObject=None):

        super().__init__(parent)

        self.i = i

    def headerData(
        self
        , section: int
        , orientation: Qt.Orientation
        , role : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if orientation == Qt.Vertical:
            return super().headerData(section, orientation, role)

        if role == Qt.DisplayRole:
            if section == 0:
                return "Secret message"
            if section == 1:
                return "Identification"

        return super().headerData(section, orientation, role)

    def rowCount(self, parent: QModelIndex=QModelIndex()):
        return self.i

    def columnCount(self, parent: QModelIndex=QModelIndex()):
        return 2

    def data(
        self
        , index: QModelIndex=QModelIndex()
        , role : Qt.ItemDataRole=Qt.DisplayRole
    ):
        if role == Qt.SizeHintRole:
            print(f"Asking for size hint on {row};{self.i}")
            return super().data(index, role)

        if role != Qt.DisplayRole:
            return QVariant()

        row, column = index.row(), index.column()

        if column == 0:
            return "Here is the message"
        if column == 1:
            return f"{row} out of {self.i}"

        return super().data(index, role)


class MyScrollWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.layout = QVBoxLayout()

        for i in range(1, 10):
            self.view = MyTableView(self)
            self.model = MyTableModel(i=i, parent=self)

            self.view.setModel(self.model)

            self.layout.addWidget(self.view)

        self.setLayout(self.layout)


class MyScrollArea(QScrollArea):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.main_widget = MyScrollWidget(self)

        self.setWidget(self.main_widget)
        self.setWidgetResizable(True)


class MyTableView(QTableView):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        vheader = self.verticalHeader()
        vheader.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.Maximum
        )

    def sizeHint(self):
        print('Asking for a size hint')

        rows = self.model().rowCount()
        height = self.verticalHeader().height()

        print(f'Will use {height}')
        print(f'Will compute to {rows * height}')

        return QSize(rows * height, 800)

    def setModel(self, model: QAbstractItemModel):

        super().setModel(model)

        rows = self.model().rowCount()
        height = self.verticalHeader().height()

        self.setMinimumSize(QSize(300, rows * height))


class MyCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.scroll_area = MyScrollArea(self)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)


class MyMainWindow(QMainWindow):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.central_widget = MyCentralWidget(self)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())
