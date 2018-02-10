import sqlalchemy

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Date, Time

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
        return id(self)


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
        return id(self)


class DateModel(Base):

    __tablename__ = 'date'

    id = Column(Integer, primary_key=True)

    date = Column(Date)

    slots = relationship('SlotModel', back_populates='date')

    def __repr__(self):
        return f'DateModel(id={self.id}, date={self.date})'

    def __eq__(self, other):
        if self.date == other.date:
            return True

        return False

    def __lt__(self, other):
        if self.date < other.date:
            return True

        return False

    def __gt__(self, other):
        if self.date > self.other:
            return True

        return False

    def __le__(self, other):
        if self.date <= other.date:
            return True

        return False

    def __ge__(self, other):
        if self.date >= other.date:
            return True

        return False

    def __hash__(self):
        return id(self)


class SlotModel(Base):
    '''
    Store first and last date and time of the recorded time segment

    Note:
        Comparison operations assume that slots are disjoint
    '''

    __tablename__ = 'slot'

    id = Column(Integer, primary_key=True)

    fst = Column(Time)
    lst = Column(Time)

    task_id = Column(Integer, ForeignKey('task.id'))
    date_id = Column(Integer, ForeignKey('date.id'))

    task = relationship('TaskModel', back_populates='slots')
    date = relationship('DateModel', back_populates='slots')

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
        return id(self)
