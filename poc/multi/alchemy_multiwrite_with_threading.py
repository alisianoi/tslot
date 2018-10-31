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


def foo(lock: Lock, session: Session):

    for i in range(50):

        tim = Tim()
        tim.name = f'foo {i}'

        session.add(tim)
        session.commit()

def bar(lock: Lock, session: Session):

    for i in range(50):

        tim = Tim()
        tim.name = f'bar {i}'

        session.add(tim)
        session.commit()

if __name__ == '__main__':

    engine = create_engine(
        f'sqlite:///{Path(Path.cwd(), Path("example.db"))}'
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionMaker = sessionmaker(bind=engine)

    session_foo = SessionMaker()
    session_bar = SessionMaker()

    lock = Lock()

    threads = [
        Thread(target=foo, args=(lock, session_foo))
        , Thread(target=bar, args=(lock, session_bar))
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
