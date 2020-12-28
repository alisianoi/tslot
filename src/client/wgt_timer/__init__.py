from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.client.common.widget.dock_widget import TDockWidget
from src.client.wgt_timer.widget.timer_controls import TTimerControlsWidget


class TTimerControlsDockWidget(TDockWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.TopDockWidgetArea)

        self.timer_controls_wgt = TTimerControlsWidget()

        self.timer_controls_wgt.requested.connect(self.handle_requested)

        self.responded.connect(self.timer_controls_wgt.handle_responded)
        self.triggered.connect(self.timer_controls_wgt.handle_triggered)

        self.setWidget(self.timer_controls_wgt)

    def kickstart(self):
        self.timer_controls_wgt.kickstart()
