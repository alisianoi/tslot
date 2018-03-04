import sqlalchemy

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Time, DateTime

from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


tags_and_tasks = Table(
    'tags_and_tasks'
    , Base.metadata
    , Column('tag_id', Integer, ForeignKey('tag.id'))
    , Column('task_id', Integer, ForeignKey('task.id'))
)


class TagModel(Base):

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    tasks = relationship(
        'TaskModel', secondary=tags_and_tasks, back_populates='tags'
    )

    def __repr__(self):
        return f'TagModel(id={self.id}, name={self.name})'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class TaskModel(Base):

    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    tags = relationship(
        'TagModel', secondary=tags_and_tasks, back_populates='tasks'
    )

    slots = relationship('SlotModel', back_populates='task')

    def __repr__(self):
        return f'TaskModel(id={self.id}, name={self.name})'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)


class SlotModel(Base):
    '''
    Store first and last date and time of the recorded time segment

    The date and time are UTC+00:00 with DST adjustment removed
    '''

    __tablename__ = 'slot'

    id = Column(Integer, primary_key=True)

    # First point in time (when the timer was started)
    fst = Column(DateTime, nullable=False)
    # Last point in time (when the timer was stopped)
    # If this is unknown, then the timer is still running
    lst = Column(DateTime, nullable=True)

    task_id = Column(Integer, ForeignKey('task.id'))

    task = relationship('TaskModel', back_populates='slots')

    def __repr__(self):
        return f'SlotModel(id={self.id}, fst={self.fst}, lst={self.lst})'

    def __eq__(self, other):
        if self.fst == other.fst and self.lst == other.lst:
            return True

        return False

    def __lt__(self, other):
        if self.lst < other.fst:
            return True

        return False

    def __gt__(self, other):
        if self.fst > other.lst:
            return True

        return False

    def __le__(self, other):
        if self.lst <= other.fst:
            return True

        return False

    def __ge__(self, other):
        if self.fst >= other.lst:
            return True

        return False

    def __hash__(self):
        return hash((self.fst, self.lst))
