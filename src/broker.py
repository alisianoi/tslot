import logging

from datetime import datetime
from pathlib import Path

from PyQt5.QtCore import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.model import Base, Tag, Task, Slot


class SlotWorker(QObject):
    '''
    Make database query in background, use Qt signals to return results

    Args:
        session  : SQLAlchemy database session instance
        date_fst : datetime after which the slots should start
        date_lst : datetime before which the slots should stop
        slice_fst: first element to be returned [1]
        slice_lst: first element to *not* be returned [1]
        parent   : parent object if Qt ownership is required

    Raises:
        RuntimeError: if date_fst > date_list

    Note:
        [1]: See http://docs.sqlalchemy.org/en/latest/orm/query.html
             to learn more about SQLAlchemy batch processing
    '''

    stored = pyqtSignal()
    loaded = pyqtSignal(list)

    started = pyqtSignal()
    stopped = pyqtSignal()
    errored = pyqtSignal()

    def __init__(
        self
        , session  : Session
        , date_fst : datetime=None
        , date_lst : datetime=None
        , slice_fst: int=0
        , slice_lst: int=100
        , parent   : QObject=None
    ):

        super().__init__(parent)

        if date_fst is not None and date_lst is not None:
            if date_fst > date_lst:
                raise RuntimeError('Must be date_fst <= date_lst')

        self.session = session
        self.date_fst, self.date_lst = date_fst, date_lst
        self.slice_fst, self.slice_lst = slice_fst, slice_lst

        self.logger = logging.getLogger('tslot')
        self.logger.debug('SlotWorker has a logger')

    @pyqtSlot()
    def work(self):
        self.logger.debug('About to emit .started')
        self.started.emit()

        self.logger.debug('About to emit .loaded')
        if self.date_fst is not None and self.date_lst is not None:
            self.loaded.emit([
                (tag, task, slot)
                for tag, task, slot in self.session.query(
                    Tag, Task, Slot
                ).filter(
                    Tag.tasks
                    , Task.slots
                    , self.date_fst <= Slot.fst
                    , Slot.lst < self.date_lst
                ).order_by(
                    Slot.fst
                ).slice(
                    self.slice_fst, self.slice_lst
                )
            ])
        else:
            self.loaded.emit([
                (tag, task, slot)
                for tag, task, slot in self.session.query(
                    Tag, Task, Slot
                ).filter(
                    Tag.tasks, Task.slots
                ).order_by(
                    Slot.fst
                ).slice(
                    self.slice_fst, self.slice_lst
                )
            ])

        self.logger.debug('About to emit .stopped')
        self.stopped.emit()


class SlotRunnable(QRunnable):

    def __init__(self, worker: SlotWorker):

        super().__init__()

        self.worker = worker

    @pyqtSlot()
    def run(self):
        self.worker.work()


class DataBroker(QObject):
    '''
    Read and write to the underlying database

    The database communication is dispatched to separate threads. This
    allows to use DataBroker inside GUI code without GUI freezing.

    Note:
        See Stylist as somewhat similar class
    '''

    def __init__(self, path: Path=None, parent: QObject=None):
        '''
        Create a (unique) database session and a (unique) threadpool

        This class is supposed to be a singleton: provide one database
        connection and one threadpool for parallel database queries.

        Args:
            path  : full path to the database; If None, use default
            parent: if Qt ownership is required, provides parent object
        '''

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        if path is None:
            path = Path(Path.cwd(), Path('tslot.db'))

        self.logger.debug('About to create_engine({})'.format(path))
        self.engine = create_engine('sqlite:///{}'.format(path))

        self.sessionmaker = sessionmaker()
        self.sessionmaker.configure(bind=self.engine)

        self.logger.debug('About to create database session')
        self.session = self.sessionmaker()

        self.logger.debug('About to create threadpool')
        self.threadpool = QThreadPool()

    def load_slots(
            self
            , fn_loaded
            , fn_started=None
            , fn_stopped=None
            , fn_errored=None
            , slice_fst: int=0
            , slice_lst: int=100
    ):
        '''
        Dispatch a slot loading task to an instance of a SlotWorker

        Args:
            fn_loaded : a callback for the loaded signal (success)
            fn_started: a callback for the started signal
            fn_stopped: a callback for the stopped signal
            fn_errored: a callback for the errored signal
            slice_fst : the first slot to actually return
            slice_lst : the first slot to *not* actually return
        '''

        if fn_started is None:
            fn_started = self.fn_started
        if fn_stopped is None:
            fn_stopped = self.fn_stopped
        if fn_errored is None:
            fn_errored = self.fn_errored

        worker = SlotWorker(
            session=self.session
            , slice_fst=slice_fst
            , slice_lst=slice_lst
            , parent=self
        )

        worker.started.connect(fn_started)
        worker.stopped.connect(fn_stopped)
        worker.errored.connect(fn_errored)

        worker.loaded.connect(fn_loaded)

        self.threadpool.start(SlotRunnable(worker))

    def store_slots(self):
        raise NotImplementedError()

    @pyqtSlot()
    def fn_started(self):
        self.logger.debug('Default fn_started')

    @pyqtSlot()
    def fn_stopped(self):
        self.logger.debug('Default fn_stopped')

    @pyqtSlot()
    def fn_errored(self):
        self.logger.debug('Default fn_errored')
