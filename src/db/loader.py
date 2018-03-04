import datetime
import logging
import operator

from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from sqlalchemy import func
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src.db.model import TaskModel, SlotModel
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
    def __init__(
        self
        , session: Session=None
        , path   : Path=None
        , parent : QObject=None
    ):

        super().__init__(parent)

        if session is None and path is None:
            return self.failed.emit(
                LoadFailed('Either session or path must be set')
            )

        if session is not None and path is not None:
            return self.failed.emit(
                LoadFailed('Failed to choose between session and path')
            )

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        self.session = session
        self.path = path
        self.query = None

    def work(self):
        return self.failed.emit(
            LoadFailed('Failed to load anything: default work method')
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

    At maximum slice_lst - slice_fst dates will be loaded.

    Args:
        dt_offset: point in time which is the origin of the ray query
        direction: general direction of the ray (into past or future)
        dates_dir: sort order of the returned dates
        times_dir: sort order of the times inside each returned date
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
        , dt_offset: datetime.datetime
        , direction: str='future_to_past'
        , dates_dir: str='future_to_past'
        , times_dir: str='past_to_future'
        , slice_fst: int=0
        , slice_lst: int=100
        , session  : Session=None
        , path     : Path=None
        , parent   : QObject=None
    ):

        super().__init__(session=session, path=path, parent=parent)

        self.dt_offset = dt_offset
        self.direction = direction
        self.dates_dir = dates_dir
        self.times_dir = times_dir
        self.slice_fst = slice_fst
        self.slice_lst = slice_lst

    @logged
    def work(self):

        known_directions = ['past_to_future', 'future_to_past']

        if self.direction not in known_directions:
            return self.failed.emit(
                LoadFailed(f'General order unknown: {self.direction}')
            )

        if self.dates_dir not in known_directions:
            return self.failed.emit(
                LoadFailed(f'Dates order unknown: {self.dates_dir}')
            )

        if self.times_dir not in known_directions:
            return self.failed.emit(
                LoadFailed(f'Times order unknown: {self.times_dir}')
            )

        if self.direction == 'past_to_future':
            key = operator.ge
        else:
            key = operator.le

        if self.dates_dir == 'past_to_future':
            dates_order = func.DATE(SlotModel.fst).asc()
        else:
            dates_order = func.DATE(SlotModel.fst).desc()

        if self.times_dir == 'past_to_future':
            times_order = func.TIME(SlotModel.fst).asc()
        else:
            times_order = func.TIME(SlotModel.fst).desc()

        # SQLite/SQLAlchemy session must be created and used by the
        # same thread. Since this object is first created in one
        # thread and then moved to another one, you must create your
        # session here (not in constructor, nor anywhere else).

        if self.session is None:
            session = self.create_session()
        else:
            session = self.session

        DateLimitQuery = session.query(
            SlotModel.fst
        ).filter(
            key(SlotModel.fst, self.dt_offset)
        ).order_by(
            dates_order
        ).distinct().slice(
            self.slice_fst, self.slice_lst
        ).subquery('DateLimitQuery')

        RayDateQuery = session.query(
            SlotModel, TaskModel
        ).filter(
            SlotModel.fst == DateLimitQuery.c.fst
            , SlotModel.task_id == TaskModel.id
        ).order_by(dates_order).order_by(times_order)

        result = RayDateQuery.all()

        self.logger.debug(RayDateQuery)
        self.logger.debug(result)

        self.loaded.emit(result)

        session.close()

        self.stopped.emit()
