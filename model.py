import sqlalchemy

from sqlalchemy import Table, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, TIMESTAMP

from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

tags_and_tasks = Table(
    'tags_and_tasks'
    , Base.metadata
    , Column('tag_id', Integer, ForeignKey('tag.id'))
    , Column('task_id', Integer, ForeignKey('task.id'))
)

class Tag(Base):

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tasks = relationship(
        'Task', secondary=tags_and_tasks, back_populates='tags'
    )

class Task(Base):

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tags = relationship(
        'Tag', secondary=tags_and_tasks, back_populates='tasks'
    )

    slots = relationship('Slot', back_populates='task')

class Slot(Base):

    __tablename__ = 'slot'

    id = Column(Integer, primary_key=True)

    fst = Column(DateTime)
    lst = Column(DateTime)

    task_id = Column(Integer, ForeignKey('task.id'))

    task = relationship('Task', back_populates='slots')
