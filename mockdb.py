#!/usr/bin/env python

from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Tag, Task, Slot


def utc_to_local(utc_dt):
    '''
    Convert UTC+00:00 time to UTC+XX:YY local time
    '''

    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tzinfo=None)


def create_a_day(session, day_offset):
    '''
    Create a single smiple day of tasks

    Note:
        Function attempts to create non-overlapping tasks. However, if
        the date changes while this function is being called several
        times, then overlapping tasks can be created. Pay attention!
    '''

    chores_tag = Tag(name='Chores')
    workout_tag = Tag(name='Workout')
    freetime_tag = Tag(name='Freetime')

    cook_task = Task(name='Cook breakfast/dinner/supper')
    shop_task = Task(name='Buy groceries')
    wash_task = Task(name='Do the washing')

    movies_task = Task(name='Watch Deadpool')
    internet_task = Task(name='Surf the web')

    aerobic_task = Task(name='Run \'em miles')
    anaerobic_task = Task(name='Lift \'em weights')

    chores_tag.tasks = [cook_task, shop_task, wash_task]
    workout_tag.tasks = [aerobic_task, anaerobic_task]
    freetime_tag.tasks = [movies_task, internet_task]

    base = datetime.utcnow()
    base = base.replace(day=base.day - day_offset)

    aerobic_slot0 = Slot(
        task=aerobic_task
        , fst=base.replace(hour=8, minute=0, second=0)
        , lst=base.replace(hour=9, minute=0, second=0)
    )

    anaerobic_slot0 = Slot(
        task=anaerobic_task
        , fst=base.replace(hour=21, minute=30, second=0)
        , lst=base.replace(hour=22, minute=0 , second=0)
    )

    shop_slot0 = Slot(
        task=shop_task
        , fst=base.replace(hour=11, minute=4, second=2)
        , lst=base.replace(hour=13, minute=8, second=9)
    )

    wash_slot0 = Slot(
        task=wash_task
        , fst=base.replace(hour=13, minute=20, second=44)
        , lst=base.replace(hour=13, minute=55, second=18)
    )

    movies_slot0 = Slot(
        task=movies_task
        , fst=base.replace(hour=19, minute=0, second=0)
        , lst=base.replace(hour=20, minute=10, second=0)
    )

    internet_slot0 = Slot(
        task=internet_task
        , fst=base.replace(hour=15, minute=20, second=2)
        , lst=base.replace(hour=18, minute=33, second=2)
    )

    cook_slot0 = Slot(
        task=cook_task
        , fst=base.replace(hour=10, minute=10, second=10)
        , lst=base.replace(hour=10, minute=43, second=32)
    )

    cook_slot1 = Slot(
        task=cook_task
        , fst=base.replace(hour=14, minute=19, second=43)
        , lst=base.replace(hour=14, minute=55, second=22)
    )

    cook_slot2 = Slot(
        task=cook_task
        , fst=base.replace(hour=20, minute=30, second=0)
        , lst=base.replace(hour=21, minute=10, second=1)
    )

    session.add_all([chores_tag, workout_tag, freetime_tag])
    session.add_all([
        cook_task, shop_task, wash_task, aerobic_task, anaerobic_task,
        movies_task, internet_task
    ])
    session.add_all([
        cook_slot0, cook_slot1, cook_slot2, aerobic_slot0, shop_slot0,
        anaerobic_slot0, wash_slot0, movies_slot0, internet_slot0
    ])

    session.commit()


if __name__ == '__main__':

    dbpath = Path(Path.cwd(), Path('tslot.db'))

    engine = create_engine('sqlite:///{}'.format(dbpath))

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    for day in range(0, -3, -1):
        create_a_day(session, day)
