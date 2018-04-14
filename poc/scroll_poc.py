#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyScrollWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.i = 3

        self.layout = QVBoxLayout()

        self.layout.addWidget(QPushButton('0'))
        self.layout.addWidget(QPushButton('1'))
        self.layout.addWidget(QPushButton('2'))

        self.setStyleSheet('background-color: red')

        self.setLayout(self.layout)

    def show_next(self):
        
        self.layout.addWidget(QPushButton(str(self.i)))

        self.i += 1


class MyScrollArea(QScrollArea):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.wgt = MyScrollWidget(self)

        self.setWidget(self.wgt)
        self.setWidgetResizable(True)

        self.setLayout(self.layout)

    def event(self, event: QEvent):

        if isinstance(event, QWheelEvent):

            self.widget().show_next()

        return super().event(event)


class MyCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.layout.addWidget(QPushButton('Hello, world!'))
        self.layout.addWidget(MyScrollArea(self))

        self.setLayout(self.layout)


class MyMainWindow(QMainWindow):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.wgt = MyCentralWidget(self)

        self.setCentralWidget(self.wgt)

if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())
