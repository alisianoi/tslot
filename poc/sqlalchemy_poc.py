#!/usr/bin/env python

import pprint

import sqlalchemy

from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import cast, func, asc, desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, relationship

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import DATE, TIME
from sqlalchemy.types import Integer, String, Date, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class MySlot(Base):

    __tablename__ = 'slot'

    id = Column(Integer, primary_key=True)

    fst = Column(DateTime)
    lst = Column(DateTime)

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

    dt = datetime(year=2010, month=6, day=15, tzinfo=timezone.utc)

    fst0 = dt.replace(hour=5)
    lst0 = dt.replace(hour=6)

    fst1 = dt.replace(hour=19)
    lst1 = dt.replace(hour=20)

    slot0 = MySlot(fst=fst0, lst=lst0)
    slot1 = MySlot(fst=fst1, lst=lst1)

    session.add_all([slot0, slot1])

    query = session.query(MySlot).order_by(
        cast(MySlot.fst, DATE).asc(), cast(MySlot.fst, TIME).desc()
    )

    print(query)
    print(query.all())

    query = session.query(MySlot).order_by(
        func.DATE(MySlot.fst).asc(), func.TIME(MySlot.fst).desc()
    )

    print(query)
    print(query.all())


