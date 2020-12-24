from pathlib import Path

from PyQt5.QtCore import pyqtSlot

from src.common.logger import logged
from src.common.request import TRequest
from src.common.request.fetch.slot_fetch_request import TRaySlotFetchRequest
from src.common.request.fetch.slot_fetch_request import TRaySlotWithTagFetchRequest  # NOQA
from src.common.request.fetch.timer_fetch_request import TTimerFetchRequest
from src.common.request.stash.timer_stash_request import TTimerStashRequest
from src.db.reader_for_timer import TTimerReader
from src.db.worker import TReader
from src.db.worker import TWorker
from src.db.worker import TWriter
from src.db.writer_for_timer import TTimerWriter


class TServerController:
    def __init__(self, path: Path = None):
        if path is None:
            path = Path(Path.cwd(), Path("tslot.db"))

        self.path = path

    def handle(self, request: TRequest) -> None:
        """Find a suitable controller for the request to the database"""

        if isinstance(request, TTimerFetchRequest):
            return self.handle_timer_fetch_request(request)

        if isinstance(request, TTimerStashRequest):
            return self.handle_timer_stash_request(request)

        if isinstance(request, TRaySlotFetchRequest):
            return self.handle_ray_slot_fetch(request)

        if isinstance(request, TRaySlotWithTagFetchRequest):
            return self.handle_ray_slot_with_tag_fetch(request)

        raise RuntimeError(f"Unknown database request:\n {request}")

    def handle_timer_fetch_request(self, request: TTimerFetchRequest):
        self.dispatch_reader(TTimerReader(request, self.path, parent=self))

    def handle_timer_stash_request(self, request: TTimerStashRequest):
        self.dispatch_writer(TTimerWriter(request, self.path, parent=self))

    def handle_ray_slot_fetch(self, request: TRaySlotFetchRequest):
        self.dispatch_reader(TRaySlotReader(request, self.path, parent=self))

    def handle_ray_slot_with_tag_fetch(self, request: TRaySlotWithTagFetchRequest):
        self.dispatch_reader(TRaySlotWithTagReader(request, self.path, parent=self))

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
        self.logger.debug("Default fn_started")

    @logged
    @pyqtSlot()
    def fn_stopped(self):
        self.logger.debug("Default fn_stopped")
