#!/usr/bin/env python

import sys

from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QMainWindow, QShortcut, QWidget


class MyMainWidget(QWidget):

    def __init__(self, parent: QWidget=None) -> None:

        super().__init__(parent)

        self.trigger_shortcut = QShortcut(
            QKeySequence(Qt.CTRL + Qt.Key_P), self
        )

        self.trigger_shortcut.activated.connect(
            self.tell_me
        )

    @pyqtSlot()
    def tell_me(self):
        print('BONANZA!')


class MyMainWindow(QMainWindow):

    def __init__(self, parent: QWidget=None) -> None:

        super().__init__(parent)

        self.widget = MyMainWidget()

        self.setCentralWidget(self.widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MyMainWindow()
    main_window.show()

    sys.exit(app.exec())
