from pathlib import Path

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThreadPool, QRunnable

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Tag, Task, Slot


class SlotWorker(QObject):

    started = pyqtSignal()
    errored = pyqtSignal()
    stopped = pyqtSignal()

    loaded = pyqtSignal(list)
    stored = pyqtSignal(list)

    def __init__(self, parent: QObject=None):

        super().__init__(parent)

    def work(self):
        self.started.emit()

        # self.loaded.emit(
        #     [(tag, task, slot) for tag, task, slot in self.session.query(Tag, Task, Slot).filter(Tag.tasks, Task.slots).order_by(Slot.fst)]
        # )

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

        # if path is None:
        #     path = Path(Path.cwd(), Path('timereaper.db'))

        # self.engine = create_engine('sqlite:///{}'.format(path))

        # self.sessionmaker = sessionmaker()
        # self.sessionmaker.configure(bind=self.engine)

        self.threadpool = QThreadPool()

    def load_slots(self, fn_started, fn_stopped):
        # worker = SlotDAO()

        # worker.signals.started.connect(fn_started)
        # worker.signals.stopped.connect(fn_stopped)

        # worker = DataSignals(self)

        # worker.started.connect(fn_started)
        # worker.stopped.connect(fn_stopped)

        worker = SlotWorker()

        worker.started.connect(fn_started)
        worker.stopped.connect(fn_stopped)

        self.threadpool.start(SlotRunnable(worker))

        print('load_slots done (ok)')

    def store_data(self):
        pass
