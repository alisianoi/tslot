import datetime
import logging
import operator

from pathlib import Path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.msg.base import TRequest, TResponse, TFailure
from src.msg.fetch import TFetchRequest, TFetchResponse
from src.msg.stash import TStashRequest, TStashResponse
from src.utils import logged


class TWorker(QObject):
    '''
    Provides a set of common signals and methods for all subclasses

    This opens a brand new session every time because the SQLAlchemy
    session object should be opened and used in the same thread.

    This provides the necessary signals/slots that the business logic
    classes will trigger. Deriving classes should use those signals.

    Args:
        path   : path to the SQLite database file
        parent : parent object if Qt ownership is required
    '''

    # TODO: the two signals below are not actively used
    # Emitted before the database query
    started = pyqtSignal()
    # Emitted after the database query
    stopped = pyqtSignal()

    # Emitted if there is an error at any point
    alerted = pyqtSignal(TFailure)

    @logged
    def __init__(self, path: Path=None, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        self.path = path
        self.query = None
        self.session = None

    def work(self):
        return self.alerted.emit(
            TFailure('Failed to load anything: default work method')
        )

    @logged
    def create_session(self):
        '''
        Create an SQLite/SQLAlchemy database session
        '''

        if not isinstance(self.path, Path) or not self.path.exists():
            return self.alerted.emit(
                TFailure(f'Path to database is gone {self.path}')
            )

        self.logger.debug(f'Will create db session to {self.path}')

        # TODO: think about making SessionMaker a lot more global
        # See: http://docs.sqlalchemy.org/en/latest/orm/session_basics.html#when-do-i-make-a-sessionmaker
        engine = create_engine(f'sqlite:///{self.path}')
        SessionMaker = sessionmaker(bind=engine)

        return SessionMaker()


class TReader(TWorker):
    '''
    Provides the base class for all different *Reader classes
    '''

    fetched = pyqtSignal(TFetchResponse)

    def __init__(
        self
        , request: TFetchRequest
        , path: Path=None
        , parent: QObject=None
    ):

        super().__init__(path, parent)

        self.request = request

class TWriter(TWorker):
    '''
    Provides the base class for all different *Writer classes
    '''

    stashed = pyqtSignal(TStashResponse)

    def __init__(self, path: Path=None, parent: QObject=None):

        super().__init__(path, parent)
