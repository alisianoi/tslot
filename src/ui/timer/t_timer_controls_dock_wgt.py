from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.ui.timer.t_timer_controls_wgt import TTimerControlsWidget


class TTimerControlsDockWidget(QDockWidget):

    def __init__(self, parent: QObject=None) -> None:

        super().__init__(parent)

        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.TopDockWidgetArea)

        self.setWidget(TTimerControlsWidget(self))

