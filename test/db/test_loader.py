import pendulum
import pytest

from datetime import date, time, datetime, timedelta
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.model import Base, SlotModel, TaskModel
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


def put_one_date(session, fst, lst, name=None):

    if name is None:
        name = 'task'

    slot_model = SlotModel(fst=fst, lst=lst)
    task_model = TaskModel(name=name)

    task_model.slots = [slot_model]
    slot_model.task = task_model

    session.add_all([slot_model, task_model])
    session.commit()


def setup_one_slot_whole_date(session, dt=None):
    '''
    Put one slot into the database that will occupy the entire date
    '''

    if dt is None:
        dt = pendulum.create(year=2010, month=6, day=15, tz='utc')

    fst, lst = dt.start_of('day'), dt.end_of('day')

    put_one_date(session, fst, lst)

    return [(fst, lst)]


def setup_one_slot_one_date(session, dt=None):
    '''
    Put one one-hour slot into the database
    '''

    if dt is None:
        dt = pendulum.create(year=2010, month=6, day=15, tz='utc')

    fst = dt.replace(hour=11, minute=30, second=0, microsecond=0)
    lst = dt.replace(hour=12, minute=30, second=0, microsecond=0)

    put_one_date(session, fst, lst)

    return [(fst, lst)]


def setup_two_slots_one_date(session, dt=None):
    '''
    Put two one-hour same-date slots into the database

    Return those slots ordered past_to_future for date and for time
    '''

    if dt is None:
        dt = pendulum.create(year=2010, month=6, day=15, tz='utc')

    fst0 = dt.replace(hour=5, minute=0, second=0, microsecond=0)
    lst0 = dt.replace(hour=6, minute=0, second=0, microsecond=0)

    fst1 = dt.replace(hour=19, minute=0, second=0, microsecond=0)
    lst1 = dt.replace(hour=20, minute=0, second=0, microsecond=0)

    put_one_date(session, fst0, lst0)
    put_one_date(session, fst1, lst1)

    return [(fst0, lst0), (fst1, lst1)]


def setup_two_slots_two_dates(session, dt=None):
    '''
    Put two dates with one one-hour slot each into the database

    Return those slots ordered past_to_future for date and for time
    '''

    if dt is None:
        dt = pendulum.create(year=2010, month=6, day=15, tz='utc')

    slots = []

    for day in [10, 20]:
        slots.extend(
            setup_one_slot_one_date(session, dt.replace(day=day))
        )

    return slots


def setup_four_slots_two_dates(session, dt=None):
    '''
    Put two dates with two one-hour slots each into the database

    Return those slots ordered past_to_future for date and for time
    '''

    if dt is None:
        dt = pendulum.create(year=2010, month=6, day=15, tz='utc')

    slots = []

    for day in [10, 20]:
        slots.extend(
            setup_two_slots_one_date(session, dt.replace(day=day))
        )

    return slots


@pytest.mark.parametrize('direction, total', [
    ('past_to_future', 0), ('future_to_past', 1)
])
def test_ray_date_loader_0(session, qtbot, direction, total):

    slots = setup_one_slot_whole_date(session)

    worker = RayDateLoader(
        dt_offset=slots[0][0].add(days=1).start_of('day')
        , direction=direction
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == total

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('direction, total', [
    ('past_to_future', 1), ('future_to_past', 1)
])
def test_ray_date_loader_1(session, qtbot, direction, total):

    slots = setup_one_slot_whole_date(session)

    worker = RayDateLoader(
        dt_offset=slots[0][0].start_of('day')
        , direction=direction
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == total

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('direction, total', [
    ('past_to_future', 1), ('future_to_past', 0)
])
def test_ray_date_loader_2(session, qtbot, direction, total):

    slots = setup_one_slot_whole_date(session)

    worker = RayDateLoader(
        dt_offset=slots[0][0].subtract(days=1).start_of('day')
        , direction=direction
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == total

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('direction, total', [
    ('past_to_future', 0), ('future_to_past', 1)
])
def test_ray_date_loader_3(session, qtbot, direction, total):

    slots = setup_one_slot_one_date(session)

    worker = RayDateLoader(
        dt_offset=slots[0][0].add(days=1).start_of('day')
        , direction=direction
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == total

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('direction, total', [
    ('past_to_future', 1), ('future_to_past', 0)
])
def test_ray_date_loader_4(session, qtbot, direction, total):

    slots = setup_one_slot_one_date(session)

    worker = RayDateLoader(
        dt_offset=slots[0][0].start_of('day')
        , direction=direction
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == total

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('direction, total', [
    ('past_to_future', 1), ('future_to_past', 0)
])
def test_ray_date_loader_5(session, qtbot, direction, total):

    slots = setup_one_slot_one_date(session)

    worker = RayDateLoader(
        dt_offset=slots[0][0].subtract(days=1).start_of('day')
        , direction=direction
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == total

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('times_dir, other_dir', [
    ('past_to_future', False), ('future_to_past', True)
])
def test_ray_date_loader_times_dir_0(
    session, qtbot, times_dir, other_dir
):

    slots = setup_two_slots_one_date(session)

    worker = RayDateLoader(
        dt_offset=slots[-1][-1].add(days=1).start_of('day')
        , direction='future_to_past'
        , times_dir=times_dir
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == len(slots)

        if other_dir:
            slots.reverse()

        for entry, slot in zip(entries, slots):
            assert entry[0].fst == slot[0]
            assert entry[0].lst == slot[1]

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('times_dir, other_dir', [
    ('past_to_future', False), ('future_to_past', True)
])
def test_ray_date_loader_times_dir_1(
    session, qtbot, times_dir, other_dir
):

    slots = setup_two_slots_one_date(session)

    worker = RayDateLoader(
        dt_offset=slots[-1][-1].subtract(days=1).start_of('day')
        , direction='past_to_future'
        , times_dir=times_dir
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == len(slots)

        if other_dir:
            slots.reverse()

        for entry, slot in zip(entries, slots):
            assert entry[0].fst == slot[0]
            assert entry[0].lst == slot[1]

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('dates_dir, other_dir', [
    ('past_to_future', False), ('future_to_past', True)
])
def test_ray_date_loader_dates_dir_0(
        session, qtbot, dates_dir, other_dir
):

    slots = setup_two_slots_two_dates(session)

    worker = RayDateLoader(
        dt_offset=slots[-1][-1].add(days=1).start_of('day')
        , direction='future_to_past'
        , dates_dir=dates_dir
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == len(slots)

        if other_dir:
            slots.reverse()

        for entry, slot in zip(entries, slots):
            assert entry[0].fst == slot[0]
            assert entry[0].lst == slot[1]

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


@pytest.mark.parametrize('dates_dir, other_dir', [
    ('past_to_future', False), ('future_to_past', True)
])
def test_ray_date_loader_dates_dir_1(
        session, qtbot, dates_dir, other_dir
):

    slots = setup_two_slots_two_dates(session)

    worker = RayDateLoader(
        dt_offset=slots[0][0].subtract(days=1).start_of('day')
        , direction='past_to_future'
        , dates_dir=dates_dir
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == len(slots)

        if other_dir:
            slots.reverse()

        for entry, slot in zip(entries, slots):
            assert entry[0].fst == slot[0]
            assert entry[0].lst == slot[1]

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()
