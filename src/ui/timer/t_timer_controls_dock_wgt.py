from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.msg.base import TRequest, TResponse, TFailure
from src.ui.base import TWidget, TDockWidget
from src.ui.timer.t_timer_controls_wgt import TTimerControlsWidget


class TTimerControlsDockWidget(TDockWidget):
    """
    Provide the top-level timer area

    Although this area is dockable, its docking behavior is disabled. The
    inheritance from dockable is used to let QT control the positioning of
    several docks + main area.
    """

    def __init__(self, parent: TWidget=None) -> None:

        super().__init__(parent)

        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.TopDockWidgetArea)

        self.timer_controls_wgt = TTimerControlsWidget(self)

        self.setWidget(self.timer_controls_wgt)

        self.responded.connect(self.timer_controls_wgt.handle_responded)
        self.triggered.connect(self.timer_controls_wgt.handle_triggered)

        self.timer_controls_wgt.requested.connect(self.handle_requested)

    def kickstart(self):
        self.timer_controls_wgt.kickstart()
