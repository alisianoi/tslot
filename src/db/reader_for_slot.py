import logging
from pathlib import Path

from src.client.common import TObject
from src.common.logger import logged
from src.common.request.fetch.slot_fetch_request import TSlotFetchRequest

from src.db.worker import TReader


class TSlotReader(TReader):
    def __init__(
            self, request: TSlotFetchRequest, path: Path = None, parent: TObject = None
    ):
        super().__init__(request, path, parent)

    @logged(logger=logging.getLogger("tslot-data"), disabled=False)
    def work(self) -> None:

        if self.session is None:
            self.session = self.create_session()

        slots = self.session.query(
            SlotModel
        ).filter(
            SlotModel.lst is None
        ).all()

        if len(slots) == 0:
            self.logger.debug('No timer found')
            self.fetched.emit(TTimerFetchResponse())
        elif len(slots) == 1:
            slot = slots[0]
            task = slot.task

            timer = TEntryModel(
                slot=TSlotModel.from_model(slot),
                task=TTaskModel.from_model(task),
                tags=[TTagModel.from_model(tag) for tag in task.tags]
            )

            self.logger.debug(f"One timer found:\n{timer}")

            self.fetched.emit(TTimerFetchResponse(timer))
        else:
            self.logger.warning("Found too many active timers:")
            for slot in slots:
                self.logger.debug(slot)

            raise RuntimeError("There should be 0 or 1 active timer")

        self.session.close()

        self.stopped.emit()
