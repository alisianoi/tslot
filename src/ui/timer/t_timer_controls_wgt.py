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

    # TRequest can be one of these in requested = pyqtSignal(TRequest):
    # 1. TTimerRequest -- give me something to time, is there an active timer?
    # 2. TFetchRequest -- the user started the timer, is there any previous task/tag?
    # 3. TStoreRequest -- the user stopped the timer, please save and display?
    # 4. THintRequest -- the user is typing something, can I suggest anything?

    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent: QWidget=None):

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

    def start_timer(self):
        if self.timer_wgt.isActive():
            return

        self.timer_wgt.start_timer()
        self.push_btn.setText('Stop')

        self.started.emit()

    def stop_timer(self):
        if not self.timer_wgt.isActive():
            return

        self.timer_wgt.stop_timer()
        self.push_btn.setText('Start')

        self.stopped.emit()

    @pyqtSlot(TResponse)
    def handle_responded(self, response: TResponse) -> None:

        if isinstance(response, TTimerResponse):
            self.handle_timer_response(response)

    def handle_timer_response(self, response: TTimerResponse):

        if response.entry is None:
            return

        name = response.entry.task.name
        prd = pendulum.now() - response.entry.slot.fst

        self.task_ldt.setText(response.entry.task.name)


        # TODO: actually start the timer
