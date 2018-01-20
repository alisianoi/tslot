#!/usr/bin/env python

import sqlalchemy

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Simple(Base):

    __tablename__ = 'simple'

    id = Column(Integer, primary_key=True)

    counter = Column(Integer)

    def __eq__(self, other):
        return self.counter == other.counter

    def __lt__(self, other):
        return self.counter < other.counter

    def __le__(self, other):
        return self.counter <= other.counter

    def __gt__(self, other):
        return self.counter > other.counter

    def __ge__(self, other):
        return self.counter >= other.counter


class Slot(Base):

    __tablename__ = 'slot'

    id = Column(Integer, primary_key=True)

    name = Column(String)

    fst = Column(DateTime)
    lst = Column(DateTime)

    def __repr__(self):
        return 'Slot(name={}, fst={}, lst={})'.format(
            self.name, self.fst, self.lst
        )

    def __eq__(self, other):

        assert self.fst <= self.lst
        assert other.fst <= other.lst

        if self is other:
            return True

        if self.name != other.name:
            return False

        if self.fst != other.lst:
            return False

        if self.lst != other.lst:
            return False

        return True

    def __lt__(self, other):

        assert self.fst <= self.lst
        assert other.fst <= other.lst

        if self.lst < other.fst:
            return True

        return False

    def __le__(self, other):

        assert self.fst <= self.lst
        assert other.fst <= other.lst

        if self == other:
            return True

        if self.lst <= other.fst:
            return True

        return False

    def __gt__(self, other):

        assert self.fst <= self.lst
        assert other.fst <= other.lst

        if self.fst > other.lst:
            return True

        return False

    def __ge__(self, other):

        assert self.fst <= self.lst
        assert other.fst <= other.lst

        if self == other:
            return True

        if self.fst >= other.lst:
            return True

        return True


if __name__ == '__main__':

    base = datetime.utcnow()

    slot0 = Slot(
        name='hello'
        , fst=base.replace(hour=10, minute=10, second=10)
        , lst=base.replace(hour=10, minute=33, second=33)
    )

    slot1 = Slot(
        name='aaa'
        , fst=base.replace(hour=12, minute=12, second=12)
        , lst=base.replace(hour=12, minute=18, second=18)
    )

    for slot in sorted([slot0, slot1]):
        print(slot)
