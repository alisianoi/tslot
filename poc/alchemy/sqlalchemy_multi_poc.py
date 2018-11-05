#!/usr/bin/env python

import pprint

import multiprocessing as mp
import random
import sqlalchemy
import time
import threading

from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import Thread

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, relationship

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, String, Date, Time
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MyDate(Base):

    __tablename__ = 'date'

    id = Column(Integer, primary_key=True)

    date = Column(Date)

    slots = relationship('MySlot', back_populates='date')

    def __repr__(self):
        return f'Date(id={self.id}, date={self.date})'


class MySlot(Base):

    __tablename__ = 'slot'

    id = Column(Integer, primary_key=True)

    fst = Column(Time)
    lst = Column(Time)

    date_id = Column(Integer, ForeignKey('date.id'))
    date = relationship('MyDate', back_populates='slots')

    def __repr__(self):
        return f'MySlot(id={self.id}, fst={self.fst}, lst={self.lst})'


class MyWorker(Thread):

    def __init__(self, base, session):

        super().__init__()

        self.base = base
        self.session = session

    def run(self):

        for i in range(1, 10):
            
            date = MyDate(date=self.base.date() - timedelta(days=i - 1))

            time.sleep(random.random())

            for j in range(i):
                tm = self.base.time()
                slot = MySlot(fst=tm, lst=tm)

                date.slots.append(slot)

                self.session.add(slot)
            self.session.add(date)
            print(threading.current_thread())
            self.session.commit()


if __name__ == '__main__':

    engine = create_engine(
        f'sqlite:///{Path(Path.cwd(), Path("sqlalchemy_poc.db"))}'
        , echo=True, echo_pool=True
    )

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    SessionMaker = sessionmaker(bind=engine)

    session0 = SessionMaker()
    session1 = SessionMaker()

    base = datetime.utcnow()

    session2 = SessionMaker()
    dt = MyDate(date=base.date())
    sl = MySlot(fst=base.time(), lst=base.time())

    dt.slots.append(sl)
    session2.add(dt)
    session2.add(sl)

    print(threading.current_thread())
    worker0 = MyWorker(base, session0)
    worker1 = MyWorker(base, session1)

    worker0.start()
    worker1.start()

    worker0.join()
    worker1.join()

    session2.commit()

    # q0 = session.query(MyDate, MySlot).filter(MyDate.id == MySlot.date_id)

    # q1 = session.query(MyDate).order_by(MyDate.date.desc()).slice(5, 10).subquery()
    # q2 = session.query(q1, MySlot).filter(q1.c.id == MySlot.date_id).order_by(q1.c.date.desc(), MySlot.fst.desc())

    # q = q2

    # pprint.pprint(q.all())

    # print(f'Total {q.count()}')
    # print(q)
