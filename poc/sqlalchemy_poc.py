#!/usr/bin/env python

import pprint

import sqlalchemy

from datetime import datetime, timedelta, timezone
from pathlib import Path

from sqlalchemy import cast, func, asc, desc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, relationship

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.types import DATE, TIME
from sqlalchemy.types import Integer, String, Date, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

tags_and_slots = Table(
    'tags_and_slots'
    , Base.metadata
    , Column('tag_id', Integer, ForeignKey('tag.id'))
    , Column('slot_id', Integer, ForeignKey('slot.id'))
)


class MyTag(Base):

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    slots = relationship(
        'MySlot', secondary=tags_and_slots, back_populates='tags'
    )

    def __repr__(self):
        return f'MyTag(id={self.id}, name={self.name})'


class MySlot(Base):

    __tablename__ = 'slot'

    id = Column(Integer, primary_key=True)

    fst = Column(DateTime)
    lst = Column(DateTime)

    tags = relationship(
        'MyTag', secondary=tags_and_slots, back_populates='slots'
    )

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

    tag1 = MyTag(name='tag1')
    tag2 = MyTag(name='tag2')
    tag3 = MyTag(name='tag3')

    slot0.tags = [tag1, tag2]
    slot1.tags = [tag3]

    slots = [slot0, slot1]

    session.add_all([slot0, slot1])
    session.commit()

    SlotQuery = session.query(
        MySlot, MyTag
    ).filter(
        MySlot.id.in_([slot.id for slot in slots]), MyTag.slots
    )

    pprint.pprint(str(SlotQuery))
    pprint.pprint(SlotQuery.all())

    # TagQuery0 = session.query(MyTag).filter(MyTag.id == tags_and_slots.c.tag_id and tags_and_slots.c.slot_id == SlotQuery.c.id)
    # TagQuery1 = session.query(MySlot,MyTag).filter(MyTag.id == tags_and_slots.c.tag_id, tags_and_slots.c.slot_id == SlotQuery.c.id, MySlot.tags)

    # pprint.pprint(str(TagQuery0))
    # pprint.pprint(str(TagQuery1))

    # pprint.pprint(TagQuery0.all())
    # pprint.pprint(TagQuery1.all())

    # query = session.query(MySlot, MyTag).group_by(MySlot.id)

    # print(query)
    # pprint.pprint(query.all())

    # query = session.query(MySlot).order_by(
    #     func.DATE(MySlot.fst).asc(), func.TIME(MySlot.fst).desc()
    # )

    # print(query)
    # print(query.all())
