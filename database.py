#!/usr/bin/env python

import os

import sqlalchemy

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import Table, ForeignKey
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

association_table = Table(
    'association'
    , Base.metadata
    , Column('lft_id', Integer, ForeignKey('record.id'))
    , Column('rgt_id', Integer, ForeignKey('tag.id'))
)

class Record(Base):

    __tablename__ = 'record'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tags = relationship(
        'Tag', secondary=association_table, back_populates='records'
    )

class Tag(Base):

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    records = relationship(
        'Record', secondary=association_table, back_populates='tags'
    )


if __name__ == '__main__':

    dbpath = Path(Path.cwd(), Path('timereaper.db'))

    engine = create_engine('sqlite:///{}'.format(dbpath))

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    RecordCook = Record(name='cook')
    RecordSleep = Record(name='sleep')

    RecordStudy = Record(name='study')
    RecordExams = Record(name='exams')

    TagChores = Tag(name='chores')
    TagStudies = Tag(name='studies')

    TagChores.records = [RecordCook, RecordSleep]

    session.add_all([
        RecordCook, RecordSleep, RecordStudy, RecordExams
        , TagChores, TagStudies
    ])

    session.commit()
