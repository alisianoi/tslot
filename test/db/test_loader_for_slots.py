import pytest

from src.db.loader_for_slots import TRaySlotLoader

from test.db.test_loader import setup_one_slot_one_date
from test.db.test_loader import setup_one_slot_whole_date
from test.db.test_loader import setup_two_slots_one_date
from test.db.test_loader import setup_two_slots_two_dates
from test.db.test_loader import setup_four_slots_two_dates


@pytest.mark.parametrize('direction, total', [
    ('past_to_future', 0), ('future_to_past', 1)
])
def test_ray_date_loader_0(session, qtbot, direction, total):

    slots = setup_one_slot_whole_date(session)

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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

    worker = TRaySlotLoader(
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


def test_ray_date_loader_slice_0(session, qtbot):

    slots = setup_two_slots_two_dates(session)

    worker = TRaySlotLoader(
        dt_offset=slots[-1][-1].add(days=1).start_of('day')
        , direction='future_to_past'
        , slice_fst=0
        , slice_lst=1
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == 1

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


def test_ray_date_loader_slice_1(session, qtbot):

    slots = setup_two_slots_two_dates(session)

    worker = TRaySlotLoader(
        dt_offset=slots[0][0].subtract(days=1).start_of('day')
        , direction='past_to_future'
        , slice_fst=0
        , slice_lst=1
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == 1

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


def test_ray_date_loader_slice_2(session, qtbot):

    slots = setup_four_slots_two_dates(session)

    worker = TRaySlotLoader(
        dt_offset=slots[-1][-1].add(days=1).start_of('day')
        , direction='future_to_past'
        , slice_fst=0
        , slice_lst=1
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == 2

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()


def test_ray_date_loader_slice_3(session, qtbot):

    slots = setup_four_slots_two_dates(session)

    worker = TRaySlotLoader(
        dt_offset=slots[0][0].subtract(days=1).start_of('day')
        , direction='past_to_future'
        , slice_fst=0
        , slice_lst=1
    )

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == 2

    worker.loaded.connect(handle_loaded)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        worker.work()
