#!/usr/bin/env python

import logging
import pendulum
import sys

from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.cache import TCacheBroker
from src.db.broker import TVaultBroker
from src.font import initialize_font_databse
from src.ui.base import TWidget
from src.ui.menu.t_menu_wgt import TDockMenuWidget
from src.ui.home.t_scroll_area import TScrollArea
from src.stylist import Stylist
from src.ui.timer.t_timer_controls_dock_wgt import TTimerControlsDockWidget
from src.utils import configure_logging


class TCentralWidget(TWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.scroll = TScrollArea(parent=self)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)

        # TODO: move this into a thread
        self.stylist = Stylist(
            parent=self, path=Path(Path.cwd(), Path('css'), Path('tslot.css'))
        )

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

        self.vault = TVaultBroker(parent=self)
        self.cache = TCacheBroker(parent=self)

        self.menu = TDockMenuWidget(parent=self)
        self.timer = TTimerControlsDockWidget(parent=self)
        self.widget = TCentralWidget(parent=self)

        self.setCentralWidget(self.widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.menu)
        self.addDockWidget(Qt.TopDockWidgetArea, self.timer)

        # TODO: look into font selection
        self.setFont(QFont('Quicksand-Medium', 12))

        # Connect database vault broker and memory cache broker:
        self.vault.responded.connect(self.cache.handle_responded)
        self.vault.triggered.connect(self.cache.handle_triggered)
        self.cache.requested.connect(self.vault.handle_requested)

        # Connect memory cache broker with UI widgets
        self.cache.responded.connect(
            self.widget.scroll.widget().handle_responded
        )
        self.cache.responded.connect(
            self.timer.handle_responded
        )

        self.cache.triggered.connect(
            self.widget.scroll.widget().handle_triggered
        )
        self.cache.triggered.connect(
            self.timer.handle_triggered
        )

        self.widget.scroll.widget().requested.connect(
            self.cache.handle_requested
        )
        self.timer.requested.connect(
            self.cache.handle_requested
        )

        # Connect some more signals/slots between different widgets
        self.timer.widget().menu_btn.clicked.connect(
            self.menu.toggle_menu
        )

        # Kickstart all widgets (signals/slots are connected now)
        self.kickstart()

    def kickstart(self):

        self.widget.scroll.widget().kickstart()
        self.timer.kickstart()


if __name__ == '__main__':
    # TODO: add parameters to allow log silencing
    configure_logging()

    app = QApplication(sys.argv)

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
