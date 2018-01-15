import logging

from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThreadPool, QRunnable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Tag, Task, Slot


class SlotWorker(QObject):

    stored = pyqtSignal()
    loaded = pyqtSignal(list)

    started = pyqtSignal()
    stopped = pyqtSignal()
    errored = pyqtSignal()

    def __init__(self, session, parent: QObject=None):

        super().__init__(parent)

        self.session = session

    @pyqtSlot()
    def work(self):
        logger = logging.getLogger('tslot')
        logger.debug('About to emit .started')
        self.started.emit()

        logger.debug('About to emit .loaded')
        self.loaded.emit(
            [(tag, task, slot) for tag, task, slot in self.session.query(Tag, Task, Slot).filter(Tag.tasks, Task.slots).order_by(Slot.fst)]
        )

        logger.debug('About to emit .stopped')
        self.stopped.emit()


class SlotRunnable(QRunnable):

    def __init__(self, worker: SlotWorker):

        super().__init__()

        self.worker = worker

    @pyqtSlot()
    def run(self):
        self.worker.work()


class DataBroker(QObject):

    def __init__(self, path: Path=None, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        if path is None:
            path = Path(Path.cwd(), Path('timereaper.db'))

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
    ):

        if fn_started is None:
            fn_started = self.fn_started
        if fn_stopped is None:
            fn_stopped = self.fn_stopped
        if fn_errored is None:
            fn_errored = self.fn_errored

        worker = SlotWorker(self.session)

        worker.started.connect(fn_started)
        worker.stopped.connect(fn_stopped)
        worker.errored.connect(fn_errored)

        worker.loaded.connect(fn_loaded)

        self.threadpool.start(SlotRunnable(worker))

    def store_data(self):
        pass

    @pyqtSlot()
    def fn_started(self):
        self.logger.debug('Default fn_started')

    @pyqtSlot()
    def fn_stopped(self):
        self.logger.debug('Default fn_stopped')

    @pyqtSlot()
    def fn_errored(self):
        self.logger.debug('Default fn_errored')
