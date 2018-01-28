#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class SimpleRunnable(QRunnable):

    @pyqtSlot()
    def run(self):
        print('hello')


class DataBroker(QObject):

    def __init__(self, parent: QObject=None):

        super().__init__()

        self.threadpool = QThreadPool()

    def load_data(self):
        self.threadpool.start(SimpleRunnable())


class MCentralWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.broker = DataBroker(self)
        self.broker.load_data()

class MMainWindow(QMainWindow):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.central_widget = MCentralWidget(self)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':

    app = QApplication(sys.argv)

    main_window = MMainWindow()
    main_window.show()

    sys.exit(app.exec())
