import logging
import operator

# TODO: this could be the wrong func
from sqlalchemy.sql.functions import func

from src.common.dto.model import TEntryModel, TSlotModel, TTagModel, TTaskModel
from src.common.logger import logged
from src.common.request.fetch.slot_fetch_request import (
    TRaySlotFetchRequest, TRaySlotWithTagFetchRequest)
from src.common.response.fetch.slot_fetch_response import (
    TRaySlotFetchResponse, TRaySlotWithTagFetchResponse)
from src.db.model import SlotModel, TagModel, TaskModel
from src.server.repository import TRepository


class TSlotRepository(TRepository):
    @logged(logger=logging.getLogger("tslot-data"), disabled=True)
    def fetch_ray_slot(self, request: TRaySlotFetchRequest):
        if self.direction == "past_to_future":
            key = operator.ge
        else:
            key = operator.le

        if self.dates_dir == "past_to_future":
            dates_order = func.DATE(SlotModel.fst).asc()
        else:
            dates_order = func.DATE(SlotModel.fst).desc()

        if self.times_dir == "past_to_future":
            times_order = func.TIME(SlotModel.fst).asc()
        else:
            times_order = func.TIME(SlotModel.fst).desc()

        # TODO: the comment below may no longer be relevant/true.
        # SQLite/SQLAlchemy session must be created and used by the
        # same thread. Since this object is first created in one
        # thread and then moved to another one, you must create your
        # session here (not in constructor, nor anywhere else).

        if self.session is None:
            self.session = self.create_session()

        # First, filter out the right number of dates that are either before or
        # after the given date offset. Sort and store these dates to use later.
        DateLimitQuery = (
            self.session.query(func.DATE(SlotModel.fst).label("fst_date"))
            .filter(key(SlotModel.fst, request.dt_offset))
            .order_by(dates_order)
            .distinct()
            .slice(request.slice_fst, request.slice_lst)
            .subquery("DateLimitQuery")
        )

        # Given the right number of dates, filter out all the slots that were
        # recorded on those dates.
        RayDateQuery = (
            self.session.query(SlotModel, TaskModel)
            .filter(SlotModel.lst != None)
            .filter(
                func.DATE(SlotModel.fst) == DateLimitQuery.c.fst_date,
                SlotModel.task_id == TaskModel.id,
            )
            .order_by(dates_order)
            .order_by(times_order)
        )

        # Must convert to TEntryModel because once the session is closed, the
        # result of the query will become unreachable.
        items = [
            TEntryModel(TSlotModel.from_model(slot), TTaskModel.from_model(task))
            for (slot, task) in RayDateQuery.all()
        ]

        self.session.close()

        return TRaySlotFetchResponse.from_request(items, self.request)

    @logged(logger=logging.getLogger("tslot-data"), disabled=True)
    def fetch_ray_slot_with_tag(self, request: TRaySlotWithTagFetchRequest):
        if self.direction == "past_to_future":
            key = operator.ge
        else:
            key = operator.le

        if self.dates_dir == "past_to_future":
            dates_order = func.DATE(SlotModel.fst).asc()
        else:
            dates_order = func.DATE(SlotModel.fst).desc()

        if self.times_dir == "past_to_future":
            times_order = func.TIME(SlotModel.fst).asc()
        else:
            times_order = func.TIME(SlotModel.fst).desc()

        # TODO: maybe order most specific -> least specific tags
        tags_order = TagModel.id.asc()

        # TODO: the comment below may no longer be relevant/true.
        # SQLite/SQLAlchemy session must be created and used by the
        # same thread. Since this object is first created in one
        # thread and then moved to another one, you must create your
        # session here (not in constructor, nor anywhere else).

        if self.session is None:
            self.session = self.create_session()

        DateLimitQuery = (
            self.session.query(func.DATE(SlotModel.fst).label("fst_date"))
            .filter(SlotModel.lst != None)
            .filter(key(SlotModel.fst, request.dt_offset))
            .order_by(dates_order)
            .distinct()
            .slice(request.slice_fst, request.slice_lst)
            .subquery("DateLimitQuery")
        )

        RayDateQuery = (
            self.session.query(SlotModel, TaskModel, TagModel)
            .filter(SlotModel.lst != None)
            .filter(
                func.DATE(SlotModel.fst) == DateLimitQuery.c.fst_date,
                SlotModel.task_id == TaskModel.id,
                TaskModel.tags,
            )
            .order_by(dates_order)
            .order_by(times_order)
            .order_by(tags_order)
        )

        # Must convert to TEntryModel because once the session is closed, the
        # result of the query will become unreachable.
        items = [
            TEntryModel(
                TSlotModel.from_model(slot),
                TTaskModel.from_model(task),
                [TTagModel.from_model(tag)],
            )
            for (slot, task, tag) in RayDateQuery.all()
        ]

        self.session.close()

        return TRaySlotWithTagFetchResponse.from_request(items, self.request)
