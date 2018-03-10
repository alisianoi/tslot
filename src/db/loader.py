import datetime
import logging
import operator

from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.utils import logged


class LoadFailed(Exception):

    def __init__(self, message):

        super().__init__()

        self.logger = logging.getLogger('tslot')
        self.logger.warning('Emitting a LoadFailed:')
        self.logger.warning(message)

        self.message = message


class TLoader(QObject):
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
        , path   : Path=None
        , parent : QObject=None
    ):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')
        self.logger.debug(self.__class__.__name__ + ' has a logger')

        self.path = path
        self.query = None
        self.session = None

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
