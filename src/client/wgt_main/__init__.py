from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QShortcut, QVBoxLayout, QWidget

from src.client.common.widget import TWidget
from src.client.wgt_demo_label import TLabelDemo
from src.client.wgt_timer import TTimerControlsDockWidget
from src.client.wgt_timer_table import THomeScrollArea


class TCentralWidget(TWidget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.wgt_label_demo = TLabelDemo()
        self.scroll = THomeScrollArea(parent=self)

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.wgt_label_demo)
        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)

        # Experiment with shortcuts:
        self.show_next_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_M), self)

        self.show_next_shortcut.activated.connect(self.handle_show_next_shortcut)

        self.show_next_shortcut.activated.connect(self.scroll.handle_show_next_shortcut)

    @pyqtSlot()
    def handle_show_next_shortcut(self):
        self.logger.info("enter handle_show_next_shortcut")


class TMainWindow(QMainWindow):
    def __init__(self, parent: QWidget = None):

        super().__init__(parent)

        # self.vault = TVaultBroker(parent=self)
        # self.cache = TCacheBroker(parent=self)

        self.timer = TTimerControlsDockWidget(parent=self)
        self.widget = TCentralWidget(parent=self)

        self.setCentralWidget(self.widget)

        self.addDockWidget(Qt.TopDockWidgetArea, self.timer)

        # # Connect database vault broker and memory cache broker:
        # self.vault.responded.connect(self.cache.handle_responded)
        # self.vault.triggered.connect(self.cache.handle_triggered)
        # self.cache.requested.connect(self.vault.handle_requested)

        # # Connect memory cache broker with UI widgets
        # self.cache.responded.connect(self.widget.scroll.widget().handle_responded)
        # self.cache.responded.connect(self.timer.handle_responded)

        # self.cache.triggered.connect(self.widget.scroll.widget().handle_triggered)
        # self.cache.triggered.connect(self.timer.handle_triggered)

        # self.widget.scroll.widget().requested.connect(self.cache.handle_requested)
        # self.timer.requested.connect(self.cache.handle_requested)

        # Kickstart all widgets (signals/slots are connected now)
        # self.kickstart()

    def kickstart(self):

        self.widget.scroll.widget().kickstart()
        self.timer.kickstart()
