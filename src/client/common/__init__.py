from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from src.common.request import TRequest
from src.common.response import TResponse
from src.common.failure import TFailure


class TObject(QObject):
    """
    Base class for all objects

    Supports the request-response-trigger protocol
    TODO: link to documentation

    Supports the kickstart protocol
    TODO: link to documentation
    """

    requested = pyqtSignal(TRequest)
    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    def __init__(self, parent: QObject=None) -> None:
        super().__init__(parent)

    def kickstart(self) -> None:
        pass

    @pyqtSlot(TRequest)
    def handle_requested(self, signal: TRequest) -> None:
        self.requested.emit(signal)

    @pyqtSlot(TRequest)
    def handle_responded(self, signal: TResponse) -> None:
        self.responded.emit(signal)

    @pyqtSlot(TRequest)
    def handle_triggered(self, signal: TFailure) -> None:
        self.triggered.emit(signal)
