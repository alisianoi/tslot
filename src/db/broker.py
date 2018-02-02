import logging

from datetime import datetime, timedelta, date
from pathlib import Path

from PyQt5.QtCore import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.db.model import Base, Tag, Task, Slot


class DataLoader(QObject):
    '''
    Abstract class for database queries that happen in the background

    Args:
        session: SQLAlchemy database session instance
        parent : parent object if Qt ownership is required
    '''

    # Emitted once data is written to the database
    stored = pyqtSignal()
    # Emitted once a list of data returns from the database query 
    loaded = pyqtSignal(list)

    # Emitted before the database query
    started = pyqtSignal()
    # Emitted after the database query
    stopped = pyqtSignal()
    # Emitted if there is an error at any point
    errored = pyqtSignal()

    def __init__(self, session: Session, parent: QObject=None):

        super().__init__(parent)

        self.session = session


class SlotLoader(DataLoader):
    '''
    Perform a database query, return a limited amount of results

    Args:
        session  : SQLAlchemy database session instance
        slice_fst: index of the first element to return [1]
        slice_lst: index of the first element to *not* return [1]
        parent   : parent object if Qt ownership is required

    Note:
        [1]: See http://docs.sqlalchemy.org/en/latest/orm/query.html
             to learn more about SQLAlchemy batch processing
    '''

    def __init__(
        self
        , session  : Session
        , slice_fst: int=0
        , slice_lst: int=100
        , parent   : QObject=None
    ):

        super().__init__(session, parent)

        self.slice_fst = slice_fst
        self.slice_lst = slice_lst

    @pyqtSlot()
    def work(self):
        self.started.emit()

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

        self.stopped.emit()


class DateLoader(DataLoader):
    '''
    Perform a database query, return a limited amount of results

    Args:
        session : SQLAlchemy database session instance
        date_fst: the first date to return
        date_lst: the first date to *not* return
        parent  : parent object if Qt ownership is required
    '''

    def __init__(
        self
        , session : Session
        , date_fst: datetime=None
        , date_lst: datetime=None
        , parent  : QObject=None
    ):

        super().__init__(session, parent)

        self.date_fst = date_fst
        self.date_lst = date_lst

    @pyqtSlot()
    def work(self):
        self.started.emit()

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
            )
        ])

        self.stopped.emit()


class DataRunnable(QRunnable):
    '''
    Wrap a subclass of DataLoader and enable its execution in a thread
    '''

    def __init__(self, worker: DataLoader):

        super().__init__()

        self.worker = worker

    @pyqtSlot()
    def run(self):
        self.worker.work()


class DataBroker(QObject):
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

    def __init__(self, path: Path=None, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        if path is None:
            path = Path(Path.cwd(), Path('tslot.db'))

        self.engine = create_engine('sqlite:///{}'.format(path))

        self.sessionmaker = sessionmaker()
        self.sessionmaker.configure(bind=self.engine)

        self.session = self.sessionmaker()

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
        Dispatch a slot loading task to an instance of a SlotLoader

        Load not more than (slice_lst - slice_fst) time entries, so it
        can be used to load rather large chunks to fit in memory.

        Args:
            fn_loaded : a callback for the loaded signal
            fn_started: a callback for the started signal
            fn_stopped: a callback for the stopped signal
            fn_errored: a callback for the errored signal
            slice_fst : the first slot to return
            slice_lst : the first slot to *not* return
        '''

        self.dispatch_worker(
            SlotLoader(
                session=self.session
                , slice_fst=date_fst
                , slice_lst=date_lst
                , parent=self
            )
            , fn_loaded
            , fn_started
            , fn_stopped
            , fn_errored
        )

    def load_dates(
        self
        , fn_loaded
        , fn_started=None
        , fn_stopped=None
        , fn_errored=None
        , date_fst: date=datetime.utcnow().date()
        , date_lst: date=datetime.utcnow().date() + timedelta(days=1)
    ):
        '''
        Dispatch a slot loading task to an instance of a DateLoader

        Load *all* the time entries between the given dates

        Args:
            fn_loaded : a callback for the loaded signal
            fn_started: a callback for the started signal
            fn_stopped: a callback for the stopped signal
            fn_errored: a callback for the errored signal
            slice_fst : the first slot to return
            slice_lst : the first slot to *not* return
        '''

        self.dispatch_worker(
            DateLoader(
                session=self.session
                , date_fst=date_fst
                , date_lst=date_lst
                , parent=self
            )
            , fn_loaded
            , fn_started
            , fn_stopped
            , fn_errored
        )

    def dispatch_worker(
        self
        , worker: DataLoader
        , fn_loaded
        , fn_started=None
        , fn_stopped=None
        , fn_errored=None
    ):
        '''
        Connect worker signals to slot callbacks and start its thread
        '''

        if fn_started is None:
            fn_started = self.fn_started
        if fn_stopped is None:
            fn_stopped = self.fn_stopped
        if fn_errored is None:
            fn_errored = self.fn_errored

        worker.started.connect(fn_started)
        worker.stopped.connect(fn_stopped)
        worker.errored.connect(fn_errored)

        worker.loaded.connect(fn_loaded)

        self.threadpool.start(DataRunnable(worker))

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
