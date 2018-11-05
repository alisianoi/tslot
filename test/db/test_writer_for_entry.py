from pathlib import Path

from pendulum import DateTime

from src.ai.model import TEntryModel, TSlotModel
from src.db.writer_for_entry import TEntryWriter
from src.msg.entry_stash_request import TEntryStashRequest


def test_writer_0(session, qtbot):

    entry = TEntryModel(TSlotModel(fst=DateTime.now()))

    worker = TEntryWriter(request=TEntryStashRequest([entry]))

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

        assert item.slot.fst == entry.slot.fst

    worker.stashed.connect(handle_stashed)

    with qtbot.waitSignal(worker.stashed, timeout=1000) as blocker:
        worker.work()
