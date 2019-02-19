from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.client.common.widget import TWidget
from src.client.wgt_timer.widget.label import TTimerLabel
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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.timer = QTimer(self)

        self.tick_lbl = TTimerLabel()

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

        self.tick_lbl.setText(TTimerLabel.TIMER_IS_ZERO)

        return value

    def isActive(self) -> bool:
        return self.timer.isActive()
