#!/usr/bin/env python

import time

from pathlib import Path

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from multiprocessing import Process, Queue, Lock

Base = declarative_base()


class Tim(Base):

    __tablename__ = 'tims'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    def __repr__(self):
        return f"{self.id}: {self.name}"


def foo(queue: Queue, session: Session):

    for i in range(3):

        tim = Tim()
        tim.name = f'foo {i}'

        session.add(tim)
        session.commit()

        queue.put(tim)

    print("Evertything commited and put, about to close session")
    session.close()
    print("Session closed")

def bar(queue: Queue):

    time.sleep(3)

    for i in range(3):

        tim = queue.get()
        print(tim)

if __name__ == '__main__':

    engine = create_engine(
        f'sqlite:///{Path(Path.cwd(), Path("example.db"))}'
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionMaker = sessionmaker(bind=engine)

    session = SessionMaker()

    queue = Queue()

    processes = [
        Process(target=foo, args=(queue, session))
        , Process(target=bar, args=(queue,))
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
