from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.msg.base import TRequest, TResponse, TFailure
from src.ui.timer.t_timer_controls_wgt import TTimerControlsWidget


class TTimerControlsDockWidget(QDockWidget):
    """
    Provide the top-level timer area

    Although this area is dockable, its docking behaviors are
    disabled. The inheritance from dockable is used to let QT
    control the positioning of several docks + main area.
    """

    requested = pyqtSignal(TRequest)
    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    def __init__(self, parent: QObject=None) -> None:

        super().__init__(parent)

        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setAllowedAreas(Qt.TopDockWidgetArea)

        self.setWidget(TTimerControlsWidget(self))

