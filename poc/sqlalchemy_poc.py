#!/usr/bin/env python

import pprint

import sqlalchemy

from datetime import datetime, timedelta, timezone
from pathlib import Path

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


if __name__ == '__main__':

    engine = create_engine(
        'sqlite:///{}'.format(
            Path(Path.cwd(), Path('sqlalchemy_poc.db'))
        )
    )
    SessionMaker = sessionmaker()
    SessionMaker.configure(bind=engine)

    session = SessionMaker()

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    base = datetime.utcnow()

    for i in range(1, 10):
        date = MyDate(date=base.date() - timedelta(days=i - 1))

        for j in range(i):
            slot = MySlot(fst=base.time(), lst=base.time())

            date.slots.append(slot)

            session.add(slot)
        session.add(date)
    session.commit()

    q0 = session.query(MyDate, MySlot).filter(MyDate.id == MySlot.date_id)

    q1 = session.query(MyDate).order_by(MyDate.date.desc()).slice(5, 10).subquery()
    q2 = session.query(q1, MySlot).filter(q1.c.id == MySlot.date_id).order_by(q1.c.date.desc(), MySlot.fst.desc())

    q = q2

    pprint.pprint(q.all())

    print(f'Total {q.count()}')
    print(q)
