#!/usr/bin/env python

import sys

from time import sleep

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class MyScrollWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.i = 10

        for i in range(self.i):
            self.layout.addWidget(QPushButton(str(i)))

        self.layout.addStretch(1)

        self.setStyleSheet('background-color: red')

        self.setLayout(self.layout)

    def show_next(self):

        self.layout.takeAt(self.layout.count() - 1)

        self.layout.addWidget(QPushButton(str(self.i)))

        self.layout.addStretch(1)

        self.i += 1

    def show_prev(self):

        pass


class MyScrollArea(QScrollArea):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.wgt = MyScrollWidget(self)

        self.setWidget(self.wgt)
        self.setWidgetResizable(True)

        self.show_next_shortcut = QShortcut(
            QKeySequence(self.tr('Ctrl+m', 'Show next')), self
        )

        self.show_next_shortcut.activated.connect(
            self.handle_show_next_shortcut
        )

        self.setLayout(self.layout)

    # def event(self, event: QEvent):

    #     if isinstance(event, QWheelEvent):

    #         # self.widget().show_next()
    #         print('angle:')
    #         print(event.angleDelta())
    #         print('pixel:')
    #         print(event.pixelDelta())

    #     return super().event(event)

    def wheelEvent(self, event: QWheelEvent):

        pass

    @pyqtSlot()
    def handle_show_next_shortcut(self):

        self.wgt.show_next()

class MyCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.layout = QVBoxLayout()

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
