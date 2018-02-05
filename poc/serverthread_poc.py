#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class CacheWorker(QObject):

    loaded_next = pyqtSignal(dict)

    def __init__(self, parent: QObject=None):

        super().__init__(parent=parent)

        self.data = {'key': 42}

    @pyqtSlot()
    def load_next(self):
        print(f'Worker about to send data {self.data}')
        self.loaded_next.emit(self.data)

        print('Above wait')
        QThread.currentThread().sleep(3)
        print('Below wait')


class MCentralWidget(QWidget):

    requested_next = pyqtSignal()

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.push_btn = QPushButton('Press to query server')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.push_btn)

        self.setLayout(self.layout)

        self.push_btn.clicked.connect(self.request_next)

        self.worker = CacheWorker()
        self.requested_next.connect(self.worker.load_next)
        self.worker.loaded_next.connect(self.show_next)

        self.thread = QThread(parent=self)
        self.worker.moveToThread(self.thread)

        self.thread.start()

    def request_next(self):
        self.requested_next.emit()

    @pyqtSlot(dict)
    def show_next(self, data):
        print(f'GUI received new data: {data}')

        self.data = data

        self.data['key'] = 13


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

