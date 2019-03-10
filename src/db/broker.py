import logging
from pathlib import Path

from PyQt5.QtCore import *

from src.client.common import TObject
from src.db.reader_for_slots import TRaySlotReader, TRaySlotWithTagReader
from src.db.reader_for_timer import TTimerReader
from src.db.worker import TReader, TWorker, TWriter
from src.db.writer_for_timer import TTimerWriter
from src.common.failure import TFailure
from src.common.request import TRequest
from src.common.response import TResponse
from src.common.request.fetch import TFetchRequest
from src.common.response.fetch import TFetchResponse
from src.common.request.fetch.slot_fetch_request import *
from src.common.request.stash import TStashRequest
from src.common.response.stash import TStashResponse
from src.common.request.fetch.timer_fetch_request import TTimerFetchRequest
from src.common.request.stash.timer_stash_request import TTimerStashRequest
from src.common.logger import logged


class DataRunnable(QRunnable):
    """Wrap an instance of a TWorker and later run it in another thread"""

    def __init__(self, worker: TWorker):

        super().__init__()

        self.worker = worker

    def run(self):
        self.worker.work()


class TVaultBroker(TObject):
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

    def __init__(self, path: Path=None, parent: QObject=None):

        super().__init__(parent)

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

    @pyqtSlot(TRequest)
    def handle_requested(self, request: TRequest) -> None:
        """Find a suitable handler for the request to the database"""

        if isinstance(request, TTimerFetchRequest):
            return self.handle_timer_fetch_request(request)

        if isinstance(request, TTimerStashRequest):
            return self.handle_timer_stash_request(request)

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

    def handle_timer_fetch_request(self, request: TTimerFetchRequest):
        self.dispatch_reader(TTimerReader(request, self.path, parent=self))

    def handle_timer_stash_request(self, request: TTimerStashRequest):
        self.dispatch_writer(TTimerWriter(request, self.path, parent=self))

    def handle_ray_slot_fetch(self, request: TRaySlotFetchRequest):

        self.dispatch_reader(TRaySlotReader(request, self.path, parent=self))

    def handle_ray_slot_with_tag_fetch(self, request: TRaySlotWithTagFetchRequest):

        self.dispatch_reader(
            TRaySlotWithTagReader(request, self.path, parent=self)
        )

    @logged(disabled=True)
    def dispatch_reader(self, reader: TReader):
        """Dispatch a given reader into a separate thread"""

        reader.fetched.connect(self.handle_fetched)

        self.dispatch_worker(reader)

    @logged(disabled=True)
    def dispatch_writer(self, writer: TWriter):
        """Dispatch a given writer into a separate thread"""

        writer.stashed.connect(self.handle_stashed)

        self.dispatch_worker(writer)

    @logged(disabled=True)
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

    @logged(disabled=True)
    @pyqtSlot()
    def fn_started(self):
        self.logger.debug('Default fn_started')

    @logged
    @pyqtSlot()
    def fn_stopped(self):
        self.logger.debug('Default fn_stopped')
