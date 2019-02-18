import logging
from pathlib import Path

from PyQt5.QtCore import QObject
from sqlalchemy.orm.exc import NoResultFound

from src.db.model import SlotModel, TagModel, TaskModel
from src.db.reader_for_timer import TSlotModel, TTaskModel
from src.db.worker import TWriter
from src.common.dto.base import TFailure
from src.common.dto.timer import TTimerStashRequest
from src.common.logger import logged


class TTimerWriter(TWriter):

    def __init__(
        self
        , request: TTimerStashRequest
        , path   : Path=None
        , parent : QObject=None
    ) -> None:

        super().__init__(path, parent)

        self.tdata = request.tdata

    @logged(logger=logging.getLogger('tslot-data'), disabled=True)
    def work(self) -> None:

        if self.session is None:

            self.session = self.create_session()

        tdata, session = self.tdata, self.session

        slot, task = None, None

        # If the id has been provided, then update the value. If there is no id,
        # then create a brand new instance with the provided value.

        if tdata.slot.id is not None:
            slot = self.fetch_slot_or_none(tdata.slot)
        else:
            slot = SlotModel()

            session.add(slot)

        if slot is None:
            self.alerted.emit(TFailure(f'Could not fetch slot {tdata.slot.id}'))

            return

        slot.fst = tdata.slot.fst
        slot.lst = tdata.slot.lst

        if tdata.task.id is not None:
            task = self.fetch_task_or_none(tdata.task)
        else:
            task = TaskModel()

            session.add(task)

        if task is None:
            self.alerted.emit(TFailure(f'Could not fetch task {tdata.task.id}'))

            return

        task.name = tdata.task.name

        # tags are different:
        # 1. There could be no tags, meaning tdata.tags is []
        # 2. If there are tags present:
        #    1. Some of them could have already been assigned to this task
        #    2. Some of them could be newly assigned but pre-existing tags
        #    3. Some of them might be brand new tags that must be created
        # Note: if the user took a previously assigned tag and modified its
        # name, then it is effectively a new tag.
        tags = self.tdata.tags

        new_tags = [TagModel(name=tag.name) for tag in tags if tag.id is None]

        old_tags = session.query(
            TagModel
        ).filter(
            TagModel.id.in_([tag.id for tag in tags if tag.id is not None])
        ).all()

        # Connect slot, task and tags together:
        slot.task = task
        task.tags = new_tags + old_tags

        session.commit()

        session.close()

        self.stopped.emit()

    def fetch_slot_or_none(self, slot: TSlotModel):
        try:
            return self.session.query(
                SlotModel
            ).filter(
                SlotModel.id == slot.id
            ).one()
        except NoResultFound:
            return None

    def fetch_task_or_none(self, task: TTaskModel):
        try:
            return self.session.query(
                TaskModel
            ).filter(
                TaskModel.id == task.id
            ).one()
        except NoResultFound:
            return None
