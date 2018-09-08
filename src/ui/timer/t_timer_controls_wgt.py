import pendulum
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QHBoxLayout, QLineEdit, QPushButton

from src.ai.model import TEntryModel, TSlotModel
from src.msg.base import TResponse
from src.msg.timer import TTimerRequest, TTimerResponse, TTimerStashRequest
from src.ui.base import TWidget
from src.ui.timer.t_timer_wgt import TTimerWidget


class TTimerControlsWidget(TWidget):
    """
    Add basic controls to start/stop time tracking for a task

    Contains a line edit to name the current task and a push button to toggle
    its timer. Also holds a timer widget and a menu toggle button.
    """

    def __init__(self, parent: TWidget=None):

        super().__init__(parent)

        self.task_ldt = QLineEdit()
        self.timer_wgt = TTimerWidget()
        self.push_btn = QPushButton()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(10, 0, 10, 0)

        # The numbers at the end are stretch factors; How to do better?
        self.layout.addWidget(self.task_ldt, 7)
        self.layout.addWidget(self.timer_wgt, 1)
        self.layout.addWidget(self.push_btn, 1)

        self.setLayout(self.layout)

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

    def start_timer(self, tdata: TEntryModel=None, sleep: int=1000) -> None:
        """
        Start the timer

        Optionally, use the provided initial value as timer offset. Also, use
        custom timer sleep value if required. Finally, when restarting a timer
        from the past, use its model.

        Make sure that there is no other timer already running. When creating a
        brand new timer, make sure to save it to the database.

        :param value: initial time value
        :param sleep: sleep interval (milliseconds)
        """

        if self.timer_wgt.isActive():
            raise RuntimeError('Cannot start two timers at once')

        if tdata is None:
            value = self.start_new_timer()
        else:
            value = self.start_old_timer(tdata)

        self.timer_wgt.start_timer(value, sleep)
        self.push_btn.setText('Stop')

    def start_new_timer(self) -> int:
        tslot = TSlotModel(fst=pendulum.now(tz='UTC'))

        self.tdata = TEntryModel(slot=tslot)

        self.requested.emit(TTimerStashRequest(self.tdata))

        return 0 # zero seconds of running new timer

    def start_old_timer(self, tdata: TEntryModel) -> int:
        self.tdata = tdata

        period = pendulum.now(tz='UTC') - tdata.slot.fst

        # NOTE: .in_seconds() truncates microseconds
        return period.in_seconds()

    def stop_timer(self):
        if not self.timer_wgt.isActive():
            raise RuntimeError('Cannot stop a stopped timer')

        # NOTE: ignore the actual value
        self.timer_wgt.stop_timer()

        self.tdata.slot.lst = pendulum.now(tz='UTC')

        self.requested.emit(TTimerStashRequest(self.tdata))

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

        self.task_ldt.setText(response.entry.task.name)

        self.push_btn.setDisabled(True)

        self.start_timer(response.entry)

        self.push_btn.setDisabled(False)
