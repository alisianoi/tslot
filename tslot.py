#!/usr/bin/env python

import logging
import sys

from logging.config import dictConfig

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from broker import DataBroker
from slot import TSlotTableModel, TSlotTableView


class TTimerWidget(QWidget):

    def __init__(
            self
            , parent: QObject=None
            , timer_value: QTime=QTime(0, 0, 0, 0)
            , timer_sleep: int=1000
            , timer_format: str='hh:mm:ss'
    ):

        super().__init__(parent)

        self.timer = QTimer(self)
        self.timer_value = timer_value
        self.timer_sleep = timer_sleep
        self.timer_format = timer_format

        self.timer_lcd = QLCDNumber(self)
        self.timer_lcd.setDigitCount(len(timer_format))
        self.timer_lcd.display(timer_value.toString(timer_format))

        self.layout = QHBoxLayout(self)

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.timer_lcd)

        self.setLayout(self.layout)

        self.implement_ai()

    def implement_ai(self):
        self.timer.timeout.connect(self.update_timer)

    @pyqtSlot()
    def update_timer(self):
        self.timer_value = self.timer_value.addSecs(1)

        self.timer_lcd.display(
            self.timer_value.toString(self.timer_format)
        )

    @pyqtSlot()
    def start_timer(self):
        self.timer.setInterval(self.timer_sleep)

        self.timer.start()

    @pyqtSlot()
    def stop_timer(self):
        self.timer.stop()

        self.timer_value = QTime(0, 0, 0, 0)

        self.timer_lcd.display(
            self.timer_value.toString(self.timer_format)
        )


class TMainControlsWidget(QWidget):

    started = pyqtSignal()
    stopped = pyqtSignal()

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.ticking = False

        self.task_ldt = QLineEdit(self)
        self.timer_wdgt = TTimerWidget(self)
        self.push_btn = QPushButton(self)

        self.layout = QHBoxLayout(self)

        self.layout.addWidget(self.task_ldt, 85)
        self.layout.addWidget(self.timer_wdgt, 10)
        self.layout.addWidget(self.push_btn, 5)

        self.setLayout(self.layout)

        self.translate_ui()
        self.implement_ai()

    def translate_ui(self):
        self.task_ldt.setPlaceholderText('Type task/project')
        self.push_btn.setText('Start')

    def implement_ai(self):
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

        self.timer_wdgt.start_timer()
        self.push_btn.setText('Stop')
        self.ticking = True

        self.started.emit()

    def stop_timer(self):
        if not self.ticking:
            return

        self.timer_wdgt.stop_timer()
        self.push_btn.setText('Start')
        self.ticking = False

        self.stopped.emit()


class TCentralWidget(QWidget):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.main_controls = TMainControlsWidget(self)
        self.tslot_table_view = TSlotTableView(self)
        self.tslot_table_model = TSlotTableModel(self)

        self.tslot_table_view.setModel(self.tslot_table_model)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.main_controls)
        self.layout.addWidget(self.tslot_table_view)

        self.setLayout(self.layout)

        self.broker = DataBroker(parent=self)

        self.broker.load_slots(
            self.tslot_table_model.fn_loaded
            , self.tslot_table_model.fn_started
            , self.tslot_table_model.fn_stopped
        )


class TMainWindow(QMainWindow):

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

        self.central_widget = TCentralWidget(self)

        self.setCentralWidget(self.central_widget)


if __name__ == '__main__':
    dictConfig({
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(asctime)22s %(levelname)7s %(module)10s %(process)6d %(thread)15d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console':{
                'level':'DEBUG',
                'class':'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'tslot': {
                'handlers': ['console'],
                'level': 'DEBUG',
            }
        }
    })

    logger = logging.getLogger('tslot')
    logger.debug('Logger tslot is configured and ready')

    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
