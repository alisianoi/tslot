from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.ui.timer.t_timer_wgt import TTimerWidget


class TTimerControlsWidget(QWidget):

    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.ticking = False

        self.task_ldt = QLineEdit()
        self.timer_wgt = TTimerWidget()
        self.push_btn = QPushButton()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # The numbers at the end are stretch factors; How to do better?
        self.layout.addWidget(self.task_ldt, 7)
        self.layout.addWidget(self.timer_wgt, 1)
        self.layout.addWidget(self.push_btn, 1)

        self.setLayout(self.layout)

        font = QFont('Quicksand-Medium', 12)

        self.task_ldt.setFont(font)
        self.timer_wgt.setFont(font)
        self.push_btn.setFont(font)

        self.task_ldt.setPlaceholderText('Type task/project')
        self.push_btn.setText('Start')

        self.push_btn.clicked.connect(self.toggle_timer)

    @pyqtSlot()
    def toggle_timer(self):
        self.push_btn.setDisabled(True)

        if self.ticking:
            self.stop_timer()
        else:
            self.start_timer()

        self.push_btn.setDisabled(False)

    def start_timer(self):
        if self.ticking:
            return

        self.timer_wgt.start_timer()
        self.push_btn.setText('Stop')
        self.ticking = True

        self.started.emit()

    def stop_timer(self):
        if not self.ticking:
            return

        self.timer_wgt.stop_timer()
        self.push_btn.setText('Start')
        self.ticking = False

        self.stopped.emit()
