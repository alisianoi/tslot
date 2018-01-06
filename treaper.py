#!/usr/bin/env python

import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TrTimerWidget(QWidget):

    def __init__(self, parent: QObject=None, time_val: str='00:00:00'):

        super().__init__(parent)

        self.time_val = time_val

        self.lcd = QLCDNumber(self)
        self.lcd.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Minimum
        )

        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.lcd)

        self.setLayout(self.layout)

        self.translate_ui()
        self.implement_ai()

    def translate_ui(self):
        self.lcd.setDigitCount(len(self.time_val))
        self.lcd.display(self.time_val)

    def implement_ai(self):
        pass

    @pyqtSlot()
    def clear(self):
        self.lcd.display(self.time_val)

    @pyqtSlot()
    def display(time: str):
        self.lcd.display(self.time_val)


class TrMainControlsWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.task_ldt = QLineEdit(self)
        self.task_lcd = TrTimerWidget(self)
        self.start_btn = QPushButton(self)

        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.task_ldt, 75)
        self.layout.addWidget(self.task_lcd, 20)
        self.layout.addWidget(self.start_btn, 5)

        self.setLayout(self.layout)

        self.translate_ui()
        self.implement_ai()

    def translate_ui(self):
        self.task_ldt.setPlaceholderText('Type task/project')
        self.start_btn.setText('Start')

    def implement_ai(self):
        pass


class TrMainResultsWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

class TrCentralWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.main_controls = TrMainControlsWidget(self)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.main_controls)

        self.setLayout(self.layout)


class TrMainWindow(QMainWindow):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.central_widget = TrCentralWidget(self)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = TrMainWindow()
    main_window.show()

    sys.exit(app.exec())
