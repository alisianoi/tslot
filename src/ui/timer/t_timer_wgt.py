from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TTimerWidget(QWidget):
    """
    Keep track of a ticking timer, update label with current time

    Contains a QTimer and a QLabel to display current time value.
    QTimer is launched with the given initial value and a sleep
    interval. Each sleep interval the timer wakes up and then the
    label value is updated.

    :param value: initial QTimer value
    :param sleep: milliseconds between QTimer ticks
    """

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

        self.timer.timeout.connect(self.handle_timeout)

    @pyqtSlot()
    def handle_timeout(self):
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

    def isActive(self) -> bool:
        return self.timer.isActive()
