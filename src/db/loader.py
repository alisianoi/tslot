import logging
import operator

from datetime import datetime
from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.model import TaskModel, DateModel, SlotModel
from src.types import LoadFailed
from src.utils import logged


class DataLoader(QObject):
    '''
    Abstract class for database queries that happen in the background

    This opens a brand new session every time because the SQLAlchemy
    session object should be opened and used in the same thread.

    Args:
        path   : path to the SQLite database file
        parent : parent object if Qt ownership is required
    '''

    # Emitted once data is written to the database
    stored = pyqtSignal()
    # Emitted once a list of data returns from the database query 
    loaded = pyqtSignal(list)
    # Emitted if there is an error at any point
    failed = pyqtSignal(LoadFailed)


    # Emitted before the database query
    started = pyqtSignal()
    # Emitted after the database query
    stopped = pyqtSignal()


    @logged
    def __init__(self, path: Path, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        if path is None:
            raise RuntimeError('Path to database is None :(')

        self.path = path
        self.query = None

    def work(self):
        return self.failed.emit(
            LoadFailed('You have called default work method')
        )

    @logged
    def create_session(self):
        '''
        Create an SQLite/SQLAlchemy database session
        '''

        if not isinstance(self.path, Path) or not self.path.exists():
            return self.failed.emit(
                LoadFailed(f'Path to database is gone {self.path}')
            )

        self.logger.debug(f'Will create db session to {self.path}')

        # TODO: think about making SessionMaker a lot more global
        # See: http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-make-a-sessionmaker
        engine = create_engine(f'sqlite:///{self.path}')
        SessionMaker = sessionmaker(bind=engine)

        return SessionMaker()


class RayDateLoader(DataLoader):
    '''
    Ask database for all slots beginning from (or up to) specific date

    At maximum slice_lst - slice_fst dates will be loaded; Default
    loading direction is called 'next' but goes into the past, historic
    data. This makes sense because 'requesting next data from database'
    by default is asking about tasks recorded in the past.

    Args:
        date_offt: return dates either all >= or < this offset
        direction: go from present into past (next) or in reverse (prev)
        slice_fst: index of the first element to return [1]
        slice_lst: index of the first element to *not* return [1]
        path     : path to the SQLite database file
        parent   : parent object if Qt ownership is required

    Note:
        [1]: See http://docs.sqlalchemy.org/en/latest/orm/query.html
             to learn more about SQLAlchemy batch processing
    '''

    @logged
    def __init__(
        self
        , date_offt: datetime.date
        , direction: str='next'
        , slice_fst: int=0
        , slice_lst: int=100
        , path     : Path=None
        , parent   : QObject=None
    ):

        super().__init__(path=path, parent=parent)

        self.date_offt = date_offt
        self.direction = direction
        self.slice_fst = slice_fst
        self.slice_lst = slice_lst

    @logged
    def work(self):

        if self.direction not in ['next', 'prev']:
            return self.errored.emit(LoadFailed('Wrong direction'))

        key = operator.le if self.direction == 'next' else operator.gt

        # SQLite/SQLAlchemy session must be created and used by the
        # same thread. Since this object is first created in one
        # thread and then moved to another one, you must create your
        # session here (not in constructor, nor anywhere else).

        session = self.create_session()

        DateLimitQuery = session.query(
            DateModel
        ).filter(
            DateModel.date <= self.date_offt
        ).order_by(
            DateModel.date.desc()
        ).slice(
            self.slice_fst, self.slice_lst
        ).subquery('DateLimitQuery')

        RayDateQuery = session.query(
            DateModel, SlotModel, TaskModel
        ).filter(
            DateModel.id == DateLimitQuery.c.id
            , DateModel.id == SlotModel.date_id
            , SlotModel.task_id == TaskModel.id
        ).order_by(
            DateModel.date.desc(), SlotModel.fst.asc()
        )

        result = RayDateQuery.all()

        self.loaded.emit(result)

        session.close()

        self.stopped.emit()
