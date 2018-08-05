#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TRequest:

    def __init__(self, payload: str=None):
        if payload is None:
            self.payload = "Here is your payload"
        else:
            self.payload = payload


class TWidget(QWidget):

    requested = pyqtSignal(TRequest)

    @pyqtSlot(TRequest)
    def handle_requested(self, request: TRequest):

        print(f'You requested {request.payload}')


class TDockWidget(TWidget):

    pass

class TSubWidget0(TDockWidget):

    pass


class TSubWidget1(TDockWidget):

    pass


class TMainWindow(QWidget):

    def __init__(self, parent: QWidget=None):
        super().__init__(parent)

        self.wgt0 = TSubWidget0(self)
        self.wgt1 = TSubWidget1(self)

        self.wgt0.requested.connect(self.wgt1.handle_requested)

        self.wgt0.requested.emit(TRequest(payload='Hello, world!'))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
