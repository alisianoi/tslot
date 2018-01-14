from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Tag, Task, Slot

class DataBroker:

    def __init__(self, path: Path=None):

        if path is None:
            path = Path(Path.cwd(), Path('timereaper.db'))

        self.engine = create_engine('sqlite:///{}'.format(path))

        self.sessionmaker = sessionmaker()
        self.sessionmaker.configure(bind=self.engine)

    def load_data(self):

        session = self.sessionmaker()

        for tag, task, slot in session.query(Tag, Task, Slot).filter(Tag.tasks.id==Task.id):
            print(tag, task, slot)

    def store_data(self):
        pass

if __name__ == '__main__':
    broker = DataBroker()

    broker.load_data()
