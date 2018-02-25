#!/usr/bin/env python

import datetime
import logging
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.cache import TDataCache
from src.db.broker import TDataBroker
from src.font import initialize_font_databse
from src.scroll import TScrollArea
from src.stylist import Stylist
from src.utils import configure_logging


class TTickWidget(QWidget):
    '''
    Start a QTimer and display its results

    Args:
        timer_value: initial value for the timer
        timer_sleep: interval value between timer signals
        parent     :
    '''

    def __init__(
        self
        , timer_value: QTime=QTime(0, 0, 0, 0)
        , timer_sleep: int=1000
        , parent     : QWidget=None
    ):

        super().__init__(parent)

        self.timer = QTimer(self)
        self.timer_value = timer_value
        self.timer_sleep = timer_sleep

        self.tick_lbl = QLabel()
        self.tick_lbl.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.tick_lbl.setText(timer_value.toString())

        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.tick_lbl)

        self.setLayout(self.layout)

        self.setup_ui()
        self.setup_ai()

    def setup_ui(self):
        pass

    def setup_ai(self):
        self.timer.timeout.connect(self.update_timer)

    @pyqtSlot()
    def update_timer(self):
        self.timer_value = self.timer_value.addSecs(1)

        self.tick_lbl.setText(self.timer_value.toString())

    @pyqtSlot()
    def start_timer(self):
        self.timer.setInterval(self.timer_sleep)

        self.timer.start()

    @pyqtSlot()
    def stop_timer(self):
        self.timer.stop()

        self.timer_value = QTime(0, 0, 0, 0)

        self.tick_lbl.setText(self.timer_value.toString())

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

        self.setup_ui()
        self.setup_ai()

    def setup_ui(self):
        font = QFont('Quicksand-Medium', 12)

        self.task_ldt.setFont(font)
        self.tick_wgt.setFont(font)
        self.push_btn.setFont(font)

        self.task_ldt.setPlaceholderText('Type task/project')
        self.push_btn.setText('Start')

    def setup_ai(self):
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


class TCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        self.controls = TMainControlsWidget(parent=self)
        self.scroll = TScrollArea(parent=self)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.controls)
        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)

        self.cache = TDataCache(parent=self)
        self.broker = TDataBroker(parent=self)

        self.broker.loaded.connect(self.cache.cache)
        self.broker.failed.connect(self.cache.failed)

        self.cache.requested_next.connect(self.broker.load_next)
        self.cache.requested_prev.connect(self.broker.load_prev)
        self.cache.requested_date.connect(self.broker.load_date)
        self.cache.requested_dates.connect(self.broker.load_dates)

        self.cache.loaded.connect(self.scroll.widget.show)
        self.cache.failed.connect(self.scroll.widget.fail)

        self.scroll.widget.requested_next.connect(self.cache.load_next)
        self.scroll.widget.requested_prev.connect(self.cache.load_prev)
        self.scroll.widget.requested_date.connect(self.cache.load_date)
        self.scroll.widget.requested_dates.connect(self.cache.load_dates)

        # TODO: move this into a thread
        self.stylist = Stylist(parent=self)

        for style in self.stylist.styles:
            self.setStyleSheet(self.stylist.styles[style])

        # TODO: move this into a thread
        initialize_font_databse()


class TMainWindow(QMainWindow):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.central_widget = TCentralWidget()

        self.setCentralWidget(self.central_widget)

        self.central_widget.scroll.widget.requested_next.emit(
            datetime.datetime.utcnow().date()
        )


if __name__ == '__main__':
    # TODO: add parameters to allow log silencing
    configure_logging()

    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
