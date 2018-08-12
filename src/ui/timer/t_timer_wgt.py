from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.ui.base import TWidget
from src.utils import seconds_to_str


class TTimerWidget(TWidget):
    """
    Keep track of a ticking timer, update label with current time

    Contains a QTimer and a QLabel to display current time value. QTimer is
    launched with the given initial value and a sleep interval. Each sleep
    interval the timer wakes up and then the label value is updated.

    :param value: initial QTimer value
    :param sleep: milliseconds between QTimer ticks
    """

    TIMER_IS_ZERO = '00:00:00'

    def __init__(self, parent: TWidget=None) -> None:

        super().__init__(parent)

        self.timer = QTimer(self)

        self.tick_lbl = QLabel()
        self.tick_lbl.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.tick_lbl.setText(TTimerWidget.TIMER_IS_ZERO)

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.tick_lbl)

        self.setLayout(self.layout)

        self.timer.timeout.connect(self.handle_timeout)

    @pyqtSlot()
    def handle_timeout(self):
        self.value += self.sleep // 1000
        self.tick_lbl.setText(seconds_to_str(self.value))

    def start_timer(self, value: int=0, sleep: int=1000):
        """
        Start the timer with the given initial value and sleep interval

        :param value: initial number of elapsed seconds
        :param sleep: sleep interval (milliseconds)
        """

        self.value = value
        self.sleep = sleep

        self.tick_lbl.setText(seconds_to_str(self.value))

        self.timer.setInterval(sleep)
        self.timer.start()

    def stop_timer(self) -> QTime:
        self.timer.stop()

        value, self.value = self.value, 0

        self.tick_lbl.setText(TTimerWidget.TIMER_IS_ZERO)

        return value

    def setFont(self, font: QFont):
        self.tick_lbl.setFont(font)

    def isActive(self) -> bool:
        return self.timer.isActive()
