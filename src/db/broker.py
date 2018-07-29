import datetime
import pendulum
import logging

from pathlib import Path

from PyQt5.QtCore import *

from src.db.worker import TWorker, TReader, TWriter
from src.db.reader_for_slots import TRaySlotReader, TRaySlotWithTagReader

from src.msg.base import TRequest, TResponse, TFailure
from src.msg.fetch import TFetchRequest, TFetchResponse
from src.msg.stash import TStashRequest, TStashResponse
from src.msg.slot_fetch_request import TRaySlotFetchRequest, TRaySlotWithTagFetchRequest

from src.utils import logged


class DataRunnable(QRunnable):
    """
    Store an instance of a TWorker and later run it in another thread
    """

    def __init__(self, worker: TWorker):

        super().__init__()

        self.worker = worker

    def run(self):
        self.worker.work()


class TDiskBroker(QObject):
    """
    Provide (unique) database session and (unique) threadpool

    The database communication is dispatched to separate threads. This
    means that the GUI can call potentially long-running operations and
    not run the risk of freezing to death.

    This class is supposed to be a singleton.

    Args:
        path  : full path to the database; If None, use default
        parent: if Qt ownership is required, provides parent object
    """

    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    def __init__(self, path: Path=None, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        if path is None:
            path = Path(Path.cwd(), Path('tslot.db'))

        self.path = path

        self.threadpool = QThreadPool(parent)

    def __del__(self):
        """Wait for all the threads to finish"""

        # This avoids a 1 in 10k deadlock which would sometimes happen.
        # See: https://github.com/pytest-dev/pytest-qt/issues/199

        # Parent QObject has no __del__, so no super().__del__() here

        self.threadpool.waitForDone()

    @logged
    @pyqtSlot(TRequest)
    def handle_requested(self, request: TRequest) -> None:
        """Find a suitable handler for the request to the database"""

        if isinstance(request, TRaySlotFetchRequest):
            return self.handle_ray_slot_fetch(request)

        if isinstance(request, TRaySlotWithTagFetchRequest):
            return self.handle_ray_slot_with_tag_fetch(request)

        raise RuntimeError(f'Unknown database request:\n {request}')

    @pyqtSlot(TFetchResponse)
    def handle_fetched(self, response: TFetchResponse) -> None:
        """Forward the database response for a fetch request"""

        self.responded.emit(response)

    @pyqtSlot(TStashResponse)
    def handle_stashed(self, response: TStashResponse) -> None:
        """Forward the database response for a stash request"""

        self.responded.emit(response)

    @pyqtSlot(TFailure)
    def handle_alerted(self, failure: TFailure) -> None:
        """Forward the database failure for some previous request"""

        self.triggered.emit(failure)

    @logged
    def handle_ray_slot_fetch(
        self, request: TRaySlotFetchRequest
    ) -> None:

        self.dispatch_reader(
            TRaySlotReader(request, self.path, parent=self)
        )

    @logged
    def handle_ray_slot_with_tag_fetch(
            self, request: TRaySlotWithTagFetchRequest
    ) -> None:

        self.dispatch_reader(
            TRaySlotWithTagReader(request, self.path, parent=self)
        )

    @logged
    def dispatch_reader(self, reader: TReader):
        """Dispatch a given reader into a separate thread"""

        reader.fetched.connect(self.handle_fetched)

        self.dispatch_worker(reader)

    @logged
    def dispatch_writer(self, writer: TWriter):
        """Dispatch a given writer into a separate thread"""

        writer.stashed.connect(self.handle_stashed)

        self.dispatch_worker(writer)

    @logged
    def dispatch_worker(self, worker: TWorker):
        """
        Dispatch a given worker into a separate thread

        The worker-specific signals should already have been connected. Connect
        the signals/slots that are common to all workers and then dispatch.

        Args:
            worker: the worker to be dispatched
        """

        worker.alerted.connect(self.handle_alerted)

        worker.started.connect(self.fn_started)
        worker.stopped.connect(self.fn_stopped)

        self.threadpool.start(DataRunnable(worker))

    @logged
    @pyqtSlot()
    def fn_started(self):
        self.logger.debug('Default fn_started')

    @logged
    @pyqtSlot()
    def fn_stopped(self):
        self.logger.debug('Default fn_stopped')
