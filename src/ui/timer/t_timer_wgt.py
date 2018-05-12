from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TTimerWidget(QWidget):
    '''
    Start a QTimer and display the ticking time

    Args:
        value: initial value for the timer
        sleep: interval value between timer signals (1 second)
    '''

    stopped = pyqtSignal(QTime)

    def __init__(
        self
        , value : QTime=QTime(0, 0, 0, 0)
        , sleep : int=1000
        , parent: QWidget=None
    ) -> None:

        super().__init__(parent)

        self.timer = QTimer(self)
        self.value = value
        self.sleep = sleep

        self.tick_lbl = QLabel()
        self.tick_lbl.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.tick_lbl.setText(value.toString())

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.tick_lbl)

        self.setLayout(self.layout)

        self.timer.timeout.connect(self.update_timer)

    @pyqtSlot()
    def update_timer(self):
        self.value = self.value.addSecs(1)

        self.tick_lbl.setText(self.value.toString())

    @pyqtSlot()
    def start_timer(self):
        self.timer.setInterval(self.sleep)

        self.timer.start()

    @pyqtSlot()
    def stop_timer(self):
        self.timer.stop()

        self.stopped.emit(self.value)

        self.value = QTime(0, 0, 0, 0)

        self.tick_lbl.setText(self.value.toString())

    def setFont(self, font: QFont):
        self.tick_lbl.setFont(font)
