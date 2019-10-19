import logging

from pathlib import Path

from src.common.logger import logged, logdata


class TRepository:
    def __init__(self, path: Path = None):
        """
        Initialize a database worker

        Args:
            path: path to the SQLite database file
        """

        self.path = path
        self.query = None
        self.session = None

    @logged(logger=logging.getLogger("tslot-data"), disabled=True)
    def create_session(self):
        """Open a brand new SQLite/SQLAlchemy database session"""

        if not isinstance(self.path, Path) or not self.path.exists():
            raise TFailure(f"Path to database is gone {self.path}")

        logdata.debug(f"Will create db session to {self.path}")

        engine = create_engine(f"sqlite:///{self.path}")
        SessionMaker = sessionmaker(bind=engine)

        return SessionMaker()
