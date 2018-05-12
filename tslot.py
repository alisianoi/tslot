#!/usr/bin/env python

import logging
import pendulum
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.cache import TCacheBroker
from src.db.broker import TDiskBroker
from src.font import initialize_font_databse
from src.scroll import TScrollArea
from src.stylist import Stylist
from src.ui.timer.t_timer_controls_wgt import TTimerControlsWidget
from src.utils import configure_logging


class TCentralWidget(QWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        self.timer_controls = TTimerControlsWidget(parent=self)
        self.scroll = TScrollArea(parent=self)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.timer_controls)
        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)

        self.cache = TCacheBroker(parent=self)
        self.broker = TDiskBroker(parent=self)

        # Connect database and in-memory brokers:
        self.broker.responded.connect(self.cache.handle_responded)
        self.broker.triggered.connect(self.cache.handle_triggered)
        self.cache.requested.connect(self.broker.handle_requested)

        # Connect in-memory brokers and GUI widget(s):
        self.cache.responded.connect(
            self.scroll.widget().handle_responded
        )
        self.cache.triggered.connect(
            self.scroll.widget().handle_triggered
        )

        self.scroll.widget().requested.connect(
            self.cache.handle_requested
        )

        # TODO: move this into a thread
        self.stylist = Stylist(parent=self)

        for style in self.stylist.styles:
            self.setStyleSheet(self.stylist.styles[style])

        # TODO: move this into a thread
        initialize_font_databse()

        # Experiment with shortcuts:
        self.show_next_shortcut = QShortcut(
            QKeySequence(Qt.CTRL + Qt.Key_M), self
        )

        self.show_next_shortcut.activated.connect(
            self.handle_show_next_shortcut
        )

        self.show_next_shortcut.activated.connect(
            self.scroll.handle_show_next_shortcut
        )

    @pyqtSlot()
    def handle_show_next_shortcut(self):
        self.logger.info('enter handle_show_next_shortcut')



class TMainWindow(QMainWindow):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.widget = TCentralWidget()

        self.setCentralWidget(self.widget)

        # Kickstart all widgets (signals/slots are connected now)
        self.widget.scroll.widget().kickstart()


if __name__ == '__main__':
    # TODO: add parameters to allow log silencing
    configure_logging()

    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
