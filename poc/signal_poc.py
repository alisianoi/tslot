#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyWidget(QWidget):

    requested = pyqtSignal(int)

    def __init__(self, base, parent: QObject=None):

        super().__init__(parent)

        self.base = base

    def kickstart(self):

        for i in range(0, 10):
            print(f'TODO requested({self.base + i:03})')
            self.requested.emit(self.base + i)
            print(f'DONE requested({self.base + i:03})')

    @pyqtSlot(int)
    def handle_requested(self, payload: int):

        print(f'>>>> handled({payload:03})')

class MyCentralWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.worker0 = MyWidget(0, self)
        self.worker1 = MyWidget(100, self)

        self.worker0.requested.connect(self.worker1.handle_requested)
        self.worker1.requested.connect(self.worker0.handle_requested)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.worker0)
        self.layout.addWidget(self.worker1)

        self.setLayout(self.layout)

    def kickstart(self):

        self.worker0.kickstart()
        self.worker1.kickstart()


class MyMainWindow(QMainWindow):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.central_widget = MyCentralWidget(self)
        self.setCentralWidget(self.central_widget)

        self.central_widget.kickstart()


if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())
