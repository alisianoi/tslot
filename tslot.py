#!/usr/bin/env python

import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import pendulum
from src.cache import TCacheBroker
from src.db.broker import TVaultBroker
from src.font import initialize_font_databse
from src.style import StyleBroker
from src.ui.base import TWidget
from src.ui.home.t_scroll_area import THomeScrollArea
from src.ui.timer.t_timer_controls_dock_wgt import TTimerControlsDockWidget


class TDefaults:
    """Hold various default configuration parameters"""

    config_path = str(Path(Path.home(), '.config', 'tslot'))
    config_file = str(Path(config_path, 'config.yml'))


class TSettings:

    pass


class TCentralWidget(TWidget):

    def __init__(self, parent: QWidget=None):

        super().__init__(parent)

        self.scroll = THomeScrollArea(parent=self)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)

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

        self.timer = TTimerControlsDockWidget(parent=self)
        self.widget = TCentralWidget(parent=self)

        self.setCentralWidget(self.widget)

        self.addDockWidget(Qt.TopDockWidgetArea, self.timer)

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

        # Kickstart all widgets (signals/slots are connected now)
        self.kickstart()

    def kickstart(self):

        self.widget.scroll.widget().kickstart()
        self.timer.kickstart()


if __name__ == '__main__':
    ap = ArgumentParser(description="Make time-driven decision")

    ap.add_argument(
        "--profile"
        , type=str
        , nargs="?"
        , choices=["personal", "developer"]
        , default="personal"
        , help=
        """
            Select developer profile to use default config and database. This
            does not change your personal data.
        """
    )

    ap.add_argument(
        "--config", "--config-file"
        , type=str
        , nargs="?"
        , default=TDefaults.config_file
        , help="Path to your configuration file."
    )

    ap.add_argument(
        "-v", "--verbose"
        , action="count"
        , default=0
        , dest="verbose"
        , help="Write more output to console."
    )

    ap.add_argument(
        "--silent"
        , action="store_true"
        , default=False
        , help="Silence all console output."
    )

    args = ap.parse_args()

    app = QApplication(sys.argv)

    style = StyleBroker(path=Path(Path.cwd(), Path('css'), Path('tslot.css')))

    app.setStyleSheet(style.styles['tslot'])

    main_window = TMainWindow()
    main_window.show()

    sys.exit(app.exec())
