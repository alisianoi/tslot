#!/usr/bin/env python

from pathlib import Path

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from threading import Thread, Lock

Base = declarative_base()


class Tim(Base):

    __tablename__ = 'tims'

    id = Column(Integer, primary_key=True)

    name = Column(String)


def foo(lock: Lock, session: Session, name: str):

    tim = Tim(name=name)

    session.add(tim)

    lock.acquire()
    session.commit()
    lock.release()


if __name__ == '__main__':

    engine = create_engine(
        f'sqlite:///{Path(Path.cwd(), Path("example.db"))}'
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionMaker = sessionmaker(bind=engine)

    session = SessionMaker()

    lock = Lock()

    threads = [
        Thread(target=foo, args=(lock, session, name))
        for name in ["TimTheFatMan", "TimTheTatMan", "TimTheNunMan"]
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
