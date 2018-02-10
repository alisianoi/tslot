import pytest

import pprint

from datetime import datetime, timedelta, date, time
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from PyQt5.QtCore import *

from src.db.broker import DataBroker
from src.db.model import Base, TagModel, TaskModel, DateModel, SlotModel


def utc_to_local(utc_dt):
    '''
    Convert UTC+00:00 time to UTC+XX:YY local time
    '''

    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tzinfo=None)


def create_a_date(session, date: date):
    '''
    Create a single smiple day of tasks

    Note:
        Function attempts to create non-overlapping tasks. However, if
        the date changes while this function is being called several
        times, then overlapping tasks can be created. Pay attention!
    '''

    chores_tag = TagModel(name='Chores')
    health_tag = TagModel(name='Health')
    workout_tag = TagModel(name='Workout')
    freetime_tag = TagModel(name='Freetime')

    cook_task = TaskModel(name='Cook breakfast/dinner/supper')
    shop_task = TaskModel(name='Buy groceries')
    wash_task = TaskModel(name='Do the washing')

    movies_task = TaskModel(name='Watch Deadpool')
    internet_task = TaskModel(name='Surf the web')

    aerobic_task = TaskModel(name='Run \'em miles')
    anaerobic_task = TaskModel(name='Lift \'em weights')

    chores_tag.tasks = [cook_task, shop_task, wash_task]
    workout_tag.tasks = [aerobic_task, anaerobic_task]
    freetime_tag.tasks = [movies_task, internet_task]
    health_tag.tasks = [aerobic_task, anaerobic_task]

    today_date = DateModel(date=date)
    today_time = time()

    aerobic_slot0 = SlotModel(
        task=aerobic_task
        , fst=today_time.replace(hour=8, minute=0, second=0)
        , lst=today_time.replace(hour=9, minute=0, second=0)
    )

    anaerobic_slot0 = SlotModel(
        task=anaerobic_task
        , fst=today_time.replace(hour=21, minute=30, second=0)
        , lst=today_time.replace(hour=22, minute=0 , second=0)
    )

    shop_slot0 = SlotModel(
        task=shop_task
        , fst=today_time.replace(hour=11, minute=4, second=2)
        , lst=today_time.replace(hour=13, minute=8, second=9)
    )

    wash_slot0 = SlotModel(
        task=wash_task
        , fst=today_time.replace(hour=13, minute=20, second=44)
        , lst=today_time.replace(hour=13, minute=55, second=18)
    )

    movies_slot0 = SlotModel(
        task=movies_task
        , fst=today_time.replace(hour=19, minute=0, second=0)
        , lst=today_time.replace(hour=20, minute=10, second=0)
    )

    internet_slot0 = SlotModel(
        task=internet_task
        , fst=today_time.replace(hour=15, minute=20, second=2)
        , lst=today_time.replace(hour=18, minute=33, second=2)
    )

    cook_slot0 = SlotModel(
        task=cook_task
        , fst=today_time.replace(hour=10, minute=10, second=10)
        , lst=today_time.replace(hour=10, minute=43, second=32)
    )

    cook_slot1 = SlotModel(
        task=cook_task
        , fst=today_time.replace(hour=14, minute=19, second=43)
        , lst=today_time.replace(hour=14, minute=55, second=22)
    )

    cook_slot2 = SlotModel(
        task=cook_task
        , fst=today_time.replace(hour=20, minute=30, second=0)
        , lst=today_time.replace(hour=21, minute=10, second=1)
    )

    today_date.slots = [
        cook_slot0, cook_slot1, cook_slot2, aerobic_slot0, shop_slot0,
        anaerobic_slot0, wash_slot0, movies_slot0, internet_slot0
    ]

    session.add(today_date)
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

    return today_date


@pytest.fixture(scope="module")
def db(tmpdir_factory):

    path = Path(tmpdir_factory.mktemp('test', 'db'), 'test_broker.db')

    engine = create_engine(f'sqlite:///{path}')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    session = Session()

    base_date = datetime.utcnow().date()

    dates = []
    for days in range(0, 10):
        dates.append(
            create_a_date(session, base_date - timedelta(days=days))
        )

    session.commit()

    yield path, dates

    path.unlink()


def handle_load_next_errored():
    assert False


def handle_load_next_loaded_dates(stored_dates):

    def handler(loaded_dates):
        expected = []

        for sdate in stored_dates:
            for sslot in sorted(sdate.slots):
                expected.append((sdate, sslot, sslot.task))

        assert len(expected) == len(loaded_dates)

        for lft, rgt in zip(expected, loaded_dates):
            assert lft == rgt

    return handler


def test_load_next_0(db, qtbot):

    path, stored_dates = db

    # Sort them most recent date first
    stored_dates.sort(reverse=True)

    data_broker = DataBroker(path=path)

    errored = data_broker.errored
    loaded_dates = data_broker.loaded_dates

    with qtbot.waitSignal(loaded_dates, timeout=6000) as blocker:
        blocker.connect(errored)

        loaded_dates.connect(
            handle_load_next_loaded_dates([stored_dates[0]])
        )

        data_broker.load_next(
            stored_dates[0].date
            , slice_fst=0
            , slice_lst=1
        )
