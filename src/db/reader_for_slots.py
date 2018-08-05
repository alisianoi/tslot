import operator

from pathlib import Path

import pendulum

from sqlalchemy import func
from PyQt5.QtCore import QObject

from src.msg.base import TRequest, TResponse, TFailure
from src.msg.slot_fetch_request import TSlotFetchRequest, TRaySlotFetchRequest, TRaySlotWithTagFetchRequest
from src.msg.slot_fetch_response import TRaySlotFetchResponseFactory
from src.msg.slot_fetch_response import TRaySlotWithTagFetchResponseFactory

from src.db.worker import TReader
from src.db.model import SlotModel, TaskModel, TagModel


class TSlotReader(TReader):
    """Provide base class for all *SlotReader classes"""

    def __init__(
        self
        , request: TSlotFetchRequest
        , path   : Path=None
        , parent : QObject=None
    ) -> None:

        super().__init__(request=request, path=path, parent=parent)

        self.dates_dir = request.dates_dir
        self.times_dir = request.times_dir
        self.slice_fst = request.slice_fst
        self.slice_lst = request.slice_lst


# class TSegmentSlotLoader(TSlotLoader):

#     def __init__(
#         self
#         , dt_fst   : pendulum.datetime
#         , dt_lst   : pendulum.datetime
#         , dates_dir: str='past_to_future'
#         , times_dir: str='past_to_future'
#         , slice_fst: int=0
#         , slice_lst: int=32
#         , path     : Path=None
#         , parent   : QObject=None
#     ):

#         super().__init__(
#             dates_dir=dates_dir
#             , times_dir=times_dir
#             , slice_fst=slice_fst
#             , slice_lst=slice_lst
#             , path=path
#             , parent=parent
#         )

#         self.dt_fst = dt_fst
#         self.dt_lst = dt_lst

#     def work(self):

#         if self.wrong_direction(self.dates_dir):
#             return
#         if self.wrong_direction(self.times_dir):
#             return

#         if self.dates_dir == 'past_to_future':
#             dates_order = func.DATE(SlotModel.fst).asc()
#         else:
#             dates_order = func.DATE(SlotModel.fst).desc()

#         if self.times_dir == 'past_to_future':
#             times_order = func.TIME(SlotModel.fst).asc()
#         else:
#             times_order = func.TIME(SlotModel.fst).desc()

#         if self.session is None:
#             self.session = self.create_session()

#         SegmentDateQuery = self.session.query(
#             SlotModel, TaskModel
#         ).filter(
#             self.dt_fst <= SlotModel.lst or SlotModel.fst <= self.dt_lst
#             , (SlotModel.task_id == TaskModel.id)
#         ).order_by(
#             dates_order, times_order
#         )

#         result = SegmentDateQuery.all()

#         self.logger.debug(result)

#         self.loaded.emit(result)

#         self.session.close()

#         self.stopped.emit()


class TRaySlotReader(TSlotReader):

    def __init__(
        self
        , request: TRaySlotFetchRequest
        , path   : Path=None
        , parent : QObject=None
    ):

        super().__init__(request, path, parent)

        self.dt_offset = request.dt_offset
        self.direction = request.direction

    def work(self):

        if self.direction == 'past_to_future':
            key = operator.ge
        else:
            key = operator.le

        if self.dates_dir == 'past_to_future':
            dates_order = func.DATE(SlotModel.fst).asc()
        else:
            dates_order = func.DATE(SlotModel.fst).desc()

        if self.times_dir == 'past_to_future':
            times_order = func.TIME(SlotModel.fst).asc()
        else:
            times_order = func.TIME(SlotModel.fst).desc()

        # SQLite/SQLAlchemy session must be created and used by the
        # same thread. Since this object is first created in one
        # thread and then moved to another one, you must create your
        # session here (not in constructor, nor anywhere else).

        if self.session is None:
            self.session = self.create_session()

        # First, filter out the right number of dates that are either before or
        # after the given date offset. Sort and store these dates to use later.
        DateLimitQuery = self.session.query(
            func.DATE(SlotModel.fst).label('fst_date')
        ).filter(
            key(SlotModel.fst, self.dt_offset)
        ).order_by(
            dates_order
        ).distinct().slice(
            self.slice_fst, self.slice_lst
        ).subquery('DateLimitQuery')

        # Given the right number of dates, filter out all the slots that were
        # recorded on those dates.
        RayDateQuery = self.session.query(
            SlotModel, TaskModel
        ).filter(
            func.DATE(SlotModel.fst) == DateLimitQuery.c.fst_date
            , SlotModel.task_id == TaskModel.id
        ).order_by(dates_order).order_by(times_order)

        result = RayDateQuery.all()

        self.logger.debug(result)

        self.fetched.emit(
            TRaySlotFetchResponseFactory.from_request(result, self.request)
        )

        self.session.close()

        self.stopped.emit()


class TRaySlotWithTagReader(TSlotReader):

    def __init__(
        self
        , request: TRaySlotWithTagFetchRequest
        , path   : Path=None
        , parent : QObject=None
    ) -> None:

        super().__init__(request, path, parent)

        self.dt_offset = request.dt_offset
        self.direction = request.direction

    def work(self):

        if self.direction == 'past_to_future':
            key = operator.ge
        else:
            key = operator.le

        if self.dates_dir == 'past_to_future':
            dates_order = func.DATE(SlotModel.fst).asc()
        else:
            dates_order = func.DATE(SlotModel.fst).desc()

        if self.times_dir == 'past_to_future':
            times_order = func.TIME(SlotModel.fst).asc()
        else:
            times_order = func.TIME(SlotModel.fst).desc()

        # TODO: maybe order most specific -> least specific tags
        tags_order = TagModel.id.asc()

        # SQLite/SQLAlchemy session must be created and used by the
        # same thread. Since this object is first created in one
        # thread and then moved to another one, you must create your
        # session here (not in constructor, nor anywhere else).

        if self.session is None:
            self.session = self.create_session()

        DateLimitQuery = self.session.query(
            func.DATE(SlotModel.fst).label('fst_date')
        ).filter(
            key(SlotModel.fst, self.dt_offset)
        ).order_by(
            dates_order
        ).distinct().slice(
            self.slice_fst, self.slice_lst
        ).subquery('DateLimitQuery')

        RayDateQuery = self.session.query(
            SlotModel, TaskModel, TagModel
        ).filter(
            func.DATE(SlotModel.fst) == DateLimitQuery.c.fst_date
            , SlotModel.task_id == TaskModel.id
            , TaskModel.tags
        ).order_by(
            dates_order
        ).order_by(
            times_order
        ).order_by(
            tags_order
        )

        result = RayDateQuery.all()

        self.logger.debug(result)

        self.fetched.emit(
            TRaySlotWithTagFetchResponseFactory.from_request(
                items=result, request=self.request
            )
        )

        self.session.close()

        self.stopped.emit()
