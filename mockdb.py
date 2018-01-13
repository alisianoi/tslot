#!/usr/bin/env python

import os

from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Tag, Task, Slot


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tzinfo=None)

if __name__ == '__main__':

    dbpath = Path(Path.cwd(), Path('timereaper.db'))

    engine = create_engine('sqlite:///{}'.format(dbpath))

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    chores_tag = Tag(name='Chores')
    cook_task = Task(name='Cook dinner')
    shop_task = Task(name='Buy groceries')
    wash_task = Task(name='Do the washing')

    chores_tag.tasks = [cook_task, shop_task, wash_task]

    base = datetime.utcnow()

    cook_slot0 = Slot(
        task=cook_task
        , fst=base.replace(hour=10, minute=13, second=17)
        , lst=base.replace(hour=10, minute=32, second=19)
    )

    cook_slot1 = Slot(
        task=cook_task
        , fst=base.replace(hour=14, minute=3, second=22)
        , lst=base.replace(hour=15, minute=7, second=32)
    )

    cook_slot2 = Slot(
        task=cook_task
        , fst=base.replace(hour=20, minute=32, second=54)
        , lst=base.replace(hour=20, minute=58, second=21)
    )

    shop_slot0 = Slot(
        task=shop_task
        , fst=base.replace(hour=10, minute=55, second=43)
        , lst=base.replace(hour=11, minute=43, second=41)
    )

    session.add_all([chores_tag])
    session.add_all([cook_task, shop_task, wash_task])
    session.add_all([
        cook_slot0, cook_slot1, cook_slot2, shop_slot0
    ])

    session.commit()
