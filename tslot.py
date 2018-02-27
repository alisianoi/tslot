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
from src.tick import TMainControlsWidget
from src.stylist import Stylist
from src.utils import configure_logging


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
