import logging
from pathlib import Path

import pendulum
from src.ai.base import TObject
from src.ai.model import TEntryModel, TSlotModel, TTagModel, TTaskModel
from src.db.model import SlotModel
from src.db.worker import TReader
from src.msg.timer import TTimerRequest, TTimerResponse
from src.utils import logged


class TTimerReader(TReader):

    def __init__(
        self
        , request: TTimerRequest
        , path   : Path=None
        , parent : TObject=None
    ) -> None:
        super().__init__(request, path, parent)

    @logged(logger=logging.getLogger('tslot-data'), disabled=True)
    def work(self) -> None:

        if self.session is None:
            self.session = self.create_session()

        items = self.session.query(
            SlotModel
        ).filter(
            SlotModel.lst == None
        ).all()

        if len(items) == 0:
            self.fetched.emit(TTimerResponse())
        elif len(items) == 1:
            slot = items[0]
            task = slot.task
            tags = task.tags

            tslot = TSlotModel(pendulum.instance(slot.fst), None, slot.id)
            ttask = TTaskModel(task.name, task.id)
            ttags = [TTagModel(tag.name, tag.id) for tag in tags]

            entry = TEntryModel(tslot, ttask, ttags)

            self.fetched.emit(TTimerResponse(entry))
        else:
            raise RuntimeError("There should be 0 or 1 active timer")

        self.session.close()

        self.stopped.emit()
