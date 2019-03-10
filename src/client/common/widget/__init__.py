from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QWidget

from src.client.srv_color.service.color import TColorService

from src.common.request import TRequest
from src.common.response import TResponse
from src.common.failure import TFailure

class TWidget(QWidget):
    """Base class for all widgets."""

    requested = pyqtSignal(TRequest)
    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def kickstart(self):
        pass

    @pyqtSlot(TRequest)
    def handle_requested(self, signal: TRequest):
        self.requested.emit(signal)

    @pyqtSlot(TResponse)
    def handle_responded(self, signal: TResponse):
        self.responded.emit(signal)

    @pyqtSlot(TFailure)
    def handle_triggered(self, signal: TFailure):
        self.triggered.emit(signal)
