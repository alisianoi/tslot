#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class CacheWorker(QObject):

    responded_more = pyqtSignal()

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

    def run(self):
        print('CacheServer.run()')

    @pyqtSlot()
    def run_more(self):
        thread = QThread.currentThread()

        print('CacheServer.run_more()')
        print(f'CacheServer priority={thread.priority()}')
        print(f'CacheServer currentThread={thread.currentThread()}')
        print(f'CacheServer currentThreadId={thread.currentThreadId()}')

        print('above sleep')
        QThread.sleep(3)
        print('below sleep')
        

        self.responded_more.emit()    


class MCentralWidget(QWidget):

    requested_more = pyqtSignal()

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.push_btn = QPushButton('Press to start server')

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.push_btn)

        self.setLayout(self.layout)

        self.push_btn.clicked.connect(self.launch_cache_server)

        self.worker = CacheWorker()
        self.requested_more.connect(self.worker.run_more)

        self.thread = QThread(parent=self)
        self.worker.moveToThread(self.thread)

        self.thread.start()

    @pyqtSlot()
    def launch_cache_server(self):
        thread = QApplication.instance().thread()
        print(f'GUI priority={thread.priority()}')
        print(f'GUI currentThread={thread.currentThread()}')
        print(f'GUI currentThreadId={thread.currentThreadId()}')

        self.requested_more.emit()


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

