import pytest

import pprint
import sqlite3

from datetime import datetime, timedelta, date, time
from pathlib import Path
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from PyQt5.QtCore import *

from src.db.broker import TDataBroker, RayDateLoader
from src.db.model import Base
from src.db.model import TagModel, TaskModel, DateModel, SlotModel
from src.utils import configure_logging

configure_logging()

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
def setup_database():

    # path = Path(tmpdir_factory.mktemp('test', 'db'), 'test_broker.db')
    path = Path('test_broker.db').resolve()

    print(path)

    print("About to create_engine")
    engine = create_engine(f'sqlite:///{path}')

    print("About to drop/create all")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    print("About to create/configure session")
    Session = sessionmaker()
    Session.configure(bind=engine)

    print("About to create a session")
    session = Session()

    print("Base date in place")
    base_date = datetime.utcnow().date()

    print("About to create_a_date several times")
    dates = []
    for days in range(0, 10):
        dates.append(
            create_a_date(session, base_date - timedelta(days=days))
        )

    print("About to close session")
    session.close()

    return path


# class TestMyAwesomeFixture():

#     def test_foo(self, setup_database, qtbot):

#         print(setup_database)

#         if Path(setup_database).exists():
#             assert True
#         else:
#             assert False


class TestRayDateLoader:

    def test_0(self, setup_database, qtbot):

        path = Path(setup_database).resolve()

        assert path.exists()

        worker = RayDateLoader(
            date_offt = datetime.utcnow().date()
            , direction = 'next'
            , slice_fst = 0
            , slice_lst = 1
            , path = path
            , parent = None
        )

        with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
            print("About to connect to two signals")
            worker.loaded.connect(
                lambda dates: len(dates) == 9
            )
            worker.failed.connect(
                lambda: False
            )

            print("About to work")
            worker.work()

        print("TestRayDateLoader.test_0 leave")

        

# class TestDataBroker:

#     def handle_errored_fail(self):
#         assert False

#     def handle_loaded_0(self, dates):
#         pprint.pprint(dates)

#         assert len(dates) == 9

#     def test_load_next_0(self, db, qtbot):
#         print("TestDataBroker.test_load_next_0 enter")

#         path = Path('test_broker.db').resolve()

#         print("About to create data_broker")
#         data_broker = DataBroker(path=path)

#         print("About to fetch couple signals")
#         errored = data_broker.errored
#         loaded_dates = data_broker.loaded_dates

#         print("About to wait for signal")
#         with qtbot.waitSignal(loaded_dates, timeout=1000) as blocker:
#             print("About to connect three signals")
#             blocker.connect(errored)

#             errored.connect(self.handle_errored_fail)

#             loaded_dates.connect(
#                 self.handle_loaded_0
#             )

#             print("About to load_next")
#             data_broker.load_next(
#                 datetime.utcnow().date()
#                 , slice_fst=0
#                 , slice_lst=1
#             )

#         print("TestDataBroker.test_load_next_0 leave")
