#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyTableWidget(QTableWidget):

    def __init__(
        self
        , i     : int
        , row   : int=1
        , column: int=2
        , parent: QWidget=None
    ):

        super().__init__(parent=parent)

        self.i = i

        self.setRowCount(row)
        self.setColumnCount(column)

        self.setHorizontalHeaderLabels(['Message', 'Index'])

        self.setItem(0, 0, QTableWidgetItem('Super secret message'))
        self.setItem(0, 1, QTableWidgetItem(str(self.i)))

        self.verticalHeader().setMinimumSectionSize(1)

    def item(self, row: int, column: int):
        if column == 0:
            return 'Some meaningful message'
        if column == 1:
            return str(self.i)


class MyScrollArea(QScrollArea):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)


class MyWidgetHolder(QFrame):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.setLayout(self.layout)

    def addWidget(self, widget: QWidget):

        self.layout.addWidget(widget)


class MyCentralWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.scroll = MyScrollArea(self)
        self.scroll.setWidgetResizable(True)

        self.holder = MyWidgetHolder(self.scroll)

        for i in range(10):
            self.holder.addWidget(QPushButton('whatever'))

        self.scroll.setWidget(self.holder)

        self.layout.addWidget(self.scroll)

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
