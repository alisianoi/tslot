from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from src.msg.base import TRequest, TResponse, TFailure


class TCacheBroker(QObject):

    requested = pyqtSignal(TRequest)
    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

    @pyqtSlot(TRequest)
    def handle_requested(self, request: TRequest):
        # Connected to TWidget.requested
        self.requested.emit(request)

    @pyqtSlot(TResponse)
    def handle_responded(self, response: TResponse):
        # Connected to TDiskBroker.responded
        self.responded.emit(response)

    @pyqtSlot(TFailure)
    def handle_triggered(self, failure: TFailure):
        self.failed.emit(failure)
