import pytest

from datetime import date, time, timedelta
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.model import Base, DateModel, SlotModel, TaskModel
from src.db.loader import RayDateLoader
from src.utils import configure_logging


configure_logging()

path = Path('test_loader.db').resolve()


@pytest.fixture(scope='module')
def engine():

    engine = create_engine(f'sqlite:///{path}')

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    return engine


@pytest.fixture(scope='function')
def session(engine):

    connection = engine.connect()
    transaction = connection.begin()
    SessionMaker = sessionmaker(bind=connection)

    session = SessionMaker()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


def put_one_date(session, date, fst=None, lst=None, name=None):
    if fst is None:
        fst = time(0, 0)
    if lst is None:
        lst = time(23, 59)
    if name is None:
        name = 'task'

    date_model = DateModel(date=date)
    slot_model = SlotModel(fst=fst, lst=lst)
    task_model = TaskModel(name=name)

    date_model.slots = [slot_model]
    task_model.slots = [slot_model]
    slot_model.date = date_model
    slot_model.task = task_model

    session.add_all([date_model, slot_model, task_model])
    session.commit()


@pytest.mark.parametrize('date', [
    date(year=2000, month=1, day=1)
    , date(year=2000, month=1, day=2)
    , date(year=2000, month=1, day=3)
    , date(year=2000, month=1, day=10)
    , date(year=2000, month=1, day=29)
    , date(year=2000, month=1, day=30)
    , date(year=2000, month=2, day=1)
    , date(year=2000, month=2, day=15)
    , date(year=2000, month=2, day=29)
    , date(year=2000, month=6, day=15)
    , date(year=2000, month=12, day=1)
    , date(year=2000, month=12, day=31)
])
def test_ray_date_loader_0(session, qtbot, date):

    put_one_date(session, date=date)

    def handle_loaded(n):

        def foo(entries):
            assert len(entries) == n

        return foo

    worker = RayDateLoader(date_offt=date, session=session)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.loaded.connect(handle_loaded(1))

        worker.work()

    worker = RayDateLoader(
        date_offt=date + timedelta(days=1), session=session
    )

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.loaded.connect(handle_loaded(1))

        worker.work()

    worker = RayDateLoader(
        date_offt=date - timedelta(days=1), session=session
    )

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.loaded.connect(handle_loaded(0))

        worker.work()
