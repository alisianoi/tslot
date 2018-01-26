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

    def __repr__(self):
        return 'Tag(name={})'.format(self.name)


class Task(Base):

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    tags = relationship(
        'Tag', secondary=tags_and_tasks, back_populates='tasks'
    )

    slots = relationship('Slot', back_populates='task')

    def __repr__(self):
        return 'Task(name={})'.format(self.name)


class Slot(Base):
    '''
    Store first and last date and time of the recorded time segment

    Note: comparison operations assume that slots are disjoint
    '''

    __tablename__ = 'slot'

    id = Column(Integer, primary_key=True)

    fst = Column(DateTime)
    lst = Column(DateTime)

    task_id = Column(Integer, ForeignKey('task.id'))

    task = relationship('Task', back_populates='slots')

    def __repr__(self):
        return 'Slot(fst={}, lst={})'.format(self.fst, self.lst)

    def __eq__(self, other):
        if self is other:
            return True

        if self.fst != other.fst:
            return False

        if self.lst != other.lst:
            return False

        return True

    def __lt__(self, other):
        if self.lst < other.fst:
            return True

        return False

    def __le__(self, other):
        if self.lst <= other.fst:
            return True

        return False

    def __gt__(self, other):
        if self.fst > other.lst:
            return True

        return False

    def __ge__(self, other):
        if self.fst >= other.lst:
            return True

        return False

    def __contains__(self, other):
        if self.fst <= other.fst and other.lst <= self.lst:
            return True

        return False
