import logging
import pendulum

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.ui.base import TWidget
from src.ui.timer.t_timer_wgt import TTimerWidget
from src.msg.base import TRequest, TResponse, TFailure
from src.msg.timer import TTimerRequest, TTimerResponse


class TTimerControlsWidget(TWidget):
    """
    Add basic controls to start/stop time tracking for a task

    Contains a line edit to name the current task and a push button to toggle
    its timer. Also holds a timer widget and a menu toggle button.
    """

    def __init__(self, parent: TWidget=None):

        super().__init__(parent)

        self.menu_btn = QPushButton('\uf0c9')
        self.task_ldt = QLineEdit()
        self.timer_wgt = TTimerWidget()
        self.push_btn = QPushButton()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 10, 0)

        # The numbers at the end are stretch factors; How to do better?
        self.layout.addWidget(self.menu_btn, 0.5)
        self.layout.addWidget(self.task_ldt, 7)
        self.layout.addWidget(self.timer_wgt, 1)
        self.layout.addWidget(self.push_btn, 1)

        self.setLayout(self.layout)

        font = QFont('Font Awesome 5 Free-Regular-400', 12)

        self.menu_btn.setFont(font)

        font = QFont('Quicksand-Medium', 12)

        self.task_ldt.setFont(font)
        self.timer_wgt.setFont(font)
        self.push_btn.setFont(font)

        self.task_ldt.setPlaceholderText('Type task/project')
        self.push_btn.setText('Start')

        self.push_btn.clicked.connect(self.toggle_timer)

    def kickstart(self):
        self.requested.emit(TTimerRequest())

    @pyqtSlot()
    def toggle_timer(self):
        self.push_btn.setDisabled(True)

        if self.timer_wgt.isActive():
            self.stop_timer()
        else:
            self.start_timer()

        self.push_btn.setDisabled(False)

    def start_timer(self, value: QTime=QTime(0, 0, 0, 0), sleep: int=1000):
        """
        Start the timer with the given initial value and sleep interval

        :param value: initial time value
        :param sleep: sleep interval (milliseconds)
        """

        if self.timer_wgt.isActive():
            raise RuntimeError('Cannot start two timers at once')

        self.timer_wgt.start_timer(value, sleep)
        self.push_btn.setText('Stop')

    def stop_timer(self):
        if not self.timer_wgt.isActive():
            raise RuntimeError('Cannot stop a stopped timer')

        self.timer_wgt.stop_timer()
        self.push_btn.setText('Start')

    @pyqtSlot(TResponse)
    def handle_responded(self, response: TResponse) -> None:

        if isinstance(response, TTimerResponse):
            self.handle_timer_response(response)

    def handle_timer_response(self, response: TTimerResponse):

        if response.entry is None:
            return # database stores no active timer, nothing to do

        if self.timer_wgt.isActive():
            raise RuntimeError('Two active timers: one from DB, one from GUI')

        self.push_btn.setDisabled(True)

        self.tdata = response.entry

        self.task_ldt.setText(self.tdata.task.name)

        # TODO: time between now and the actual start of QTimer will be wasted
        period = pendulum.now(tz='UTC') - self.tdata.slot.fst

        value = QTime(
            period.hours
            , period.minutes
            , period.remaining_seconds
            , period.microseconds // 1000
        )

        self.start_timer(value)

        self.push_btn.setDisabled(False)
