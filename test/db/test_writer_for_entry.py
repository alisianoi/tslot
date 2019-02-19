from builtins import TypeError
from pathlib import Path

import pytest

import pendulum
from pendulum import DateTime
from src.common.dto.model import TEntryModel, TSlotModel, TTaskModel
from src.db.writer_for_entry import TEntryWriter
from src.common.dto.entry_stash_request import TEntryStashRequest
from src.common.dto.entry_stash_response import TEntryStashResponse


def test_writer_for_entry_0(session, qtbot):
    """Tests that a single slot with just the first time point can be stashed"""

    fst = pendulum.datetime(year=2010, month=6, day=15, tz="UTC")
    fst = fst.replace(hour=10, minute=30, second=0, microsecond=0)

    worker = TEntryWriter(TEntryStashRequest([TEntryModel(TSlotModel(fst))]))

    worker.session = session

    def handle_stashed(response):
        assert len(response.items) == 1

        item = response.items[0]

        assert item.slot is not None
        assert item.task is not None
        assert item.tags is not None

        assert item.tags == []

        assert item.slot.id is not None
        assert item.task.id is not None

        assert item.slot.fst == fst

    def handle_alerted(response):

        assert False, response

    worker.stashed.connect(handle_stashed)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.stashed, timeout=1000) as blocker:
        worker.work()


def test_writer_for_entry_1(session, qtbot):
    """Tests that a single slot with both time points can be stashed"""

    fst = pendulum.datetime(year=2010, month=6, day=15, tz="UTC")
    lst = pendulum.datetime(year=2010, month=6, day=15, tz="UTC")

    fst = fst.replace(hour=10, minute=30, second=0, microsecond=0)
    lst = lst.replace(hour=11, minute=30, second=0, microsecond=0)

    worker = TEntryWriter(
        TEntryStashRequest([TEntryModel(TSlotModel(fst, lst))])
    )

    worker.session = session

    def handle_stashed(response: TEntryStashResponse):

        assert len(response.items) == 1

        entry = response.items[0]

        assert entry.slot is not None
        assert entry.task is not None
        assert entry.tags is not None

        assert entry.slot.id is not None
        assert entry.task.id is not None

        assert entry.slot.fst is not None
        assert entry.slot.lst is not None

        assert entry.slot.fst == fst
        assert entry.slot.lst == lst

        assert entry.task.name is None

        assert entry.tags == []

    def handle_alerted(response):

        assert False, response

    worker.stashed.connect(handle_stashed)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.stashed, timeout=1000) as blocker:
        worker.work()


def test_writer_for_entry_2(session, qtbot):

    fst = pendulum.datetime(year=2010, month=6, day=15, tz="UTC")
    lst = pendulum.datetime(year=2010, month=6, day=15, tz="UTC")

    fst = fst.replace(hour=10, minute=30, second=0, microsecond=0)
    lst = lst.replace(hour=11, minute=30, second=0, microsecond=0)

    name = "Task"

    worker = TEntryWriter(
        TEntryStashRequest([TEntryModel(TSlotModel(fst, lst), TTaskModel(name))])
    )

    worker.session = session

    def handle_stashed(response: TEntryStashResponse):
        assert len(response.items) == 1

        entry = response.items[0]

        assert entry.slot is not None
        assert entry.task is not None
        assert entry.tags is not None

        assert entry.slot.id is not None
        assert entry.task.id is not None

        assert entry.slot.fst is not None
        assert entry.slot.lst is not None

        assert entry.slot.fst == fst
        assert entry.slot.lst == lst

        assert entry.task.name == name

        assert entry.tags == []

    def handle_alerted(response):

        assert False, response

    worker.stashed.connect(handle_stashed)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.stashed, timeout=1000) as blocker:
        worker.work()
