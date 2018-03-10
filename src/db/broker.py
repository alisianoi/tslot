import datetime
import logging

from pathlib import Path

from PyQt5.QtCore import *

from src.db.loader import LoadFailed, TLoader
from src.db.loader_for_slots import TRaySlotLoader

from src.utils import logged


class DataRunnable(QRunnable):
    '''
    Wrap a subclass of TLoader and enable its execution in a thread
    '''

    def __init__(self, worker: TLoader):

        super().__init__()

        self.worker = worker

    def run(self):
        self.worker.work()


class TDataBroker(QObject):
    '''
    Provide (unique) database session and (unique) threadpool

    The database communication is dispatched to separate threads. This
    means that the GUI can call potentially long-running operations and
    not run the risk of freezing to death.

    This class is supposed to be a singleton.

    Args:
        path  : full path to the database; If None, use default
        parent: if Qt ownership is required, provides parent object
    '''

    loaded = pyqtSignal(list)
    failed = pyqtSignal(LoadFailed)

    @logged
    def __init__(
        self
        , path  : Path=None
        , parent: QObject=None
    ):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        if path is None:
            path = Path(Path.cwd(), Path('tslot.db'))

        self.path = path

        self.threadpool = QThreadPool(parent)

    def __del__(self):
        '''
        Wait for all the threads to finish
        '''

        # This avoids a 1 in 10k deadlock which would sometimes happen.
        # See: https://github.com/pytest-dev/pytest-qt/issues/199

        # Parent QObject has no __del__, so no super().__del__() here

        self.threadpool.waitForDone()

    @logged
    @pyqtSlot(datetime.date)
    def load_next(
        self
        , date_offt: datetime.date=None
        , slice_fst: int=0
        , slice_lst: int=100
    ):

        if date_offt is None:
            date_offt = datetime.datetime.utcnow().date()

        self.load_ray_dates(
            date_offt
            , direction='next'
            , slice_fst=slice_fst
            , slice_lst=slice_lst
        )

    @pyqtSlot(datetime.date)
    def load_prev(
        self
        , date_offt: datetime.date=None
        , slice_fst: int=0
        , slice_lst: int=100
    ):

        if date_offt is None:
            date_offt = datetime.datetime.utcnow().date()

        self.load_ray_dates(
            date_offt
            , direction='prev'
            , slice_fst=slice_fst
            , slice_lst=slice_lst
        )

    @pyqtSlot(datetime.date)
    def load_date(self, date: datetime.date):
        pass

    @pyqtSlot(datetime.date, datetime.date)
    def load_dates(self, fst: datetime.date, lst: datetime.date):
        pass

    @logged
    def load_ray_dates(
        self
        , date_offt: datetime.date
        , direction: str='next'
        , slice_fst: int=0
        , slice_lst: int=100
    ):
        '''
        Ask for at most a few dates starting (stopping) at specific date

        Args:
            date_offt: the anchor date
            direction: loading into the future or into the past
            slice_fst: the first date to return
            slice_lst: the first date to *not* return
        '''

        if (slice_fst > slice_lst):
            return self.errored.emit('Expected slice_fst <= slice_lst')

        self.dispatch_worker(
            TRaySlotLoader(
                date_offt=date_offt
                , direction=direction
                , slice_fst=slice_fst
                , slice_lst=slice_lst
                , path=self.path
                , parent=self
            )
        )

    @logged
    def dispatch_worker(self, worker: TLoader):
        '''
        Connect worker signals to slot callbacks and start its thread
        '''

        worker.loaded.connect(self.loaded)
        worker.failed.connect(self.failed)

        worker.started.connect(self.fn_started)
        worker.stopped.connect(self.fn_stopped)

        self.threadpool.start(DataRunnable(worker))

    def store_slots(self):
        raise NotImplementedError()

    @logged
    @pyqtSlot()
    def fn_started(self):
        self.logger.debug('Default fn_started')

    @logged
    @pyqtSlot()
    def fn_stopped(self):
        self.logger.debug('Default fn_stopped')
