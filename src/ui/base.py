import logging

from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QDockWidget, QScrollArea, QTableView, QWidget

from src.msg.base import TFailure, TRequest, TResponse

# TODO: consider overriding paintEvent with the custom painting as described in:
# https://wiki.qt.io/How_to_Change_the_Background_Color_of_QWidget

# PyQt has some limitations when it comes to multiple inheritance. So, in order
# to have a common set of signals, slots and methods on the custom widgets, it
# is necessary to write some duplicated code. So here goes:


class TWidget(QWidget):
    """Base class for all widgets used by TimeSlot."""

    requested = pyqtSignal(TRequest)
    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    def __init__(self, parent: QWidget=None) -> None:
        super().__init__(parent)

        self.logger = logging.getLogger('tslot-main')

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


class TScrollArea(QScrollArea):
    """
    Base class for all scroll areas used by TimeSlot
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


class TTableView(QTableView):
    """
    Base class for all table views used by TimeSlot
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
