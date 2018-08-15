import logging

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.msg.base import TRequest, TResponse, TFailure


# PyQt has some limitations when it comes to multiple inheritance. So, in order
# to have a common set of signals, slots and methods on the custom widgets, it
# is necessary to write some duplicated code. So here goes:

class TWidget(QWidget):
    """
    Base class for all widgets used by TimeSlot

    Supports the request-response-trigger protocol
    TODO: link to documentation

    Supports the kickstart protocol
    TODO: link to documentation
    """

    requested = pyqtSignal(TRequest)
    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

    def kickstart(self) -> None:
        pass

    @pyqtSlot(TRequest)
    def handle_requested(self, signal: TRequest) -> None:
        self.requested.emit(signal)

    @pyqtSlot(TResponse)
    def handle_responded(self, signal: TResponse) -> None:
        self.responded.emit(signal)

    @pyqtSlot(TFailure)
    def handle_triggered(self, signal: TFailure) -> None:
        self.triggered.emit(signal)


class TDockWidget(QDockWidget):
    """
    Base class for all dock widgets used by TimeSlot

    Supports the request-response-trigger protocol
    TODO: link to documentation

    Supports the kickstart protocol
    TODO: link to documentation
    """

    requested = pyqtSignal(TRequest)
    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

    def kickstart(self) -> None:
        pass

    @pyqtSlot(TRequest)
    def handle_requested(self, signal: TRequest) -> None:
        self.requested.emit(signal)

    @pyqtSlot(TResponse)
    def handle_responded(self, signal: TResponse) -> None:
        self.responded.emit(signal)

    @pyqtSlot(TFailure)
    def handle_triggered(self, signal: TFailure) -> None:
        self.triggered.emit(signal)
