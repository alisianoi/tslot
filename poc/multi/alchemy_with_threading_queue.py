#!/usr/bin/env python

from pathlib import Path

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from queue import Queue
from threading import Thread, Lock

Base = declarative_base()


class Tim(Base):

    __tablename__ = 'tims'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __repr__(self):
        return f"{self.id}: {self.name}"


def foo(lock: Lock, queue: Queue, session: Session):

    for tim in session.query(Tim).all():
        queue.put(tim)

def bar(lock: Lock, queue: Queue, session: Session):

    while True:

        tim = queue.get()

        print(f"got {tim}")


if __name__ == '__main__':

    engine = create_engine(
        f'sqlite:///{Path(Path.cwd(), Path("example.db"))}'
    )

    # Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)

    SessionMaker = sessionmaker(bind=engine)

    session = SessionMaker()

    lock = Lock()
    queue = Queue()

    threads = [
        Thread(target=foo, args=(lock, queue, session))
        , Thread(target=bar, args=(lock, queue, session))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
