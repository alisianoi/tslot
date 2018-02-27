from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class TTickWidget(QWidget):
    '''
    Start a QTimer and display its results

    Args:
        value: initial value for the timer
        sleep: interval value between timer signals
        parent     :
    '''

    stopped = pyqtSignal(QTime)

    def __init__(
        self
        , value : QTime=QTime(0, 0, 0, 0)
        , sleep : int=1000
        , parent: QWidget=None
    ):

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


class TMainControlsWidget(QWidget):

    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.ticking = False

        self.task_ldt = QLineEdit()
        self.tick_wgt = TTickWidget()
        self.push_btn = QPushButton()

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # The numbers at the end are stretch factors; How to do better?
        self.layout.addWidget(self.task_ldt, 7)
        self.layout.addWidget(self.tick_wgt, 1)
        self.layout.addWidget(self.push_btn, 1)

        self.setLayout(self.layout)

        font = QFont('Quicksand-Medium', 12)

        self.task_ldt.setFont(font)
        self.tick_wgt.setFont(font)
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

        self.tick_wgt.start_timer()
        self.push_btn.setText('Stop')
        self.ticking = True

        self.started.emit()

    def stop_timer(self):
        if not self.ticking:
            return

        self.tick_wgt.stop_timer()
        self.push_btn.setText('Start')
        self.ticking = False

        self.stopped.emit()
