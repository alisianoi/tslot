import logging

import pendulum

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.msg.base import TRequest, TResponse, TFailure
from src.msg.fetch_slot import TRaySlotFetchRequest, TRaySlotFetchResponse
from src.msg.fetch_slot import TRaySlotWithTagFetchRequest, TRaySlotWithTagFetchResponse

from src.ui.home.t_table_view import TTableView
from src.ui.home.t_table_model import TTableModel

class TScrollWidget(QWidget):
    '''
    Provide the top-level widget for the scroll-enabled area

    This widget should add/remove incoming SlotTableView's, effectively
    implementing infinite scroll for a series of tables of slots.
    '''

    requested = pyqtSignal(TRequest)

    def __init__(self, parent: QWidget=None):

        super().__init__(parent=parent)

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

        self.dt_offset = pendulum.today()
        self.direction = "future_to_past"
        self.dates_dir = "future_to_past"
        self.times_dir = "future_to_past"

        self.slice_fst = 0
        self.slice_lst = 0

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.layout)

        self.kickstarted = False

    def kickstart(self):
        if self.kickstarted:
            return

        self.request(0, 1)

        self.kickstarted = True

    def request_next(self):

        self.request(self.slice_lst, self.slice_lst + 1)

    def request(self, slice_fst: int, slice_lst: int):

        request = TRaySlotWithTagFetchRequest(
              dt_offset = self.dt_offset
            , direction = self.direction
            , dates_dir = self.dates_dir
            , times_dir = self.times_dir
            , slice_fst = slice_fst
            , slice_lst = slice_lst
        )

        self.logger.info(request)

        self.requested.emit(request)

    @pyqtSlot(TResponse)
    def handle_responded(self, response: TResponse):

        if isinstance(response, TRaySlotFetchResponse):

            return self.handle_ray_slot_fetch(response)

        if isinstance(response, TRaySlotWithTagFetchResponse):

            return self.handle_ray_slot_with_tag_fetch(response)

        self.logger.info(f'{self.name} skips {response}')

    def handle_ray_slot_fetch(
            self, response: TRaySlotFetchResponse
    ) -> None:

        self.logger.info(f'{self.name} handles {response}')

        if response.is_empty():
            return

        if self.direction != response.direction:
            # widget's data direction and response's data direction are
            # not the same; Cannot use response data, so discard it
            return

        if self.times_dir != response.times_dir:
            response.in_times_dir(self.times_dir)

        if self.dates_dir != response.dates_dir:
            response.in_dates_dir(self.dates_dir)

        for day in response.break_by_date():
            fst_slot, lst_slot = day

            view = TTableView(self)
            model = TTableModel(response.items[fst_slot:lst_slot])

            view.setModel(model)

            self.show_next(view)

        if response.slice_fst < self.slice_fst:
            self.slice_fst = response.slice_fst
        if response.slice_lst > self.slice_lst:
            self.slice_lst = response.slice_lst

    def handle_ray_slot_with_tag_fetch(
            self, response: TRaySlotWithTagFetchResponse
    ) -> None:

        self.logger.info(f'{self.name} handles {response}')

        if response.is_empty():
            return

        if self.direction != response.direction:
            # widget's data direction and response's data direction are
            # not the same; Cannot use response data, so discard it
            return

        if self.times_dir != response.times_dir:
            response.in_times_dir(self.times_dir)

        if self.dates_dir != response.dates_dir:
            response.in_dates_dir(self.dates_dir)

        for day in response.break_by_date():
            fst_slot, lst_slot = day

            view = TTableView(self)
            model = TTableModel(response.items[fst_slot:lst_slot])

            view.setModel(model)

            self.show_next(view)

        if response.slice_fst < self.slice_fst:
            self.slice_fst = response.slice_fst
        if response.slice_lst > self.slice_lst:
            self.slice_lst = response.slice_lst

    def show_next(self, view: TTableView):

        # TODO: why does inserting now work?
        # Remove the spacer that props widgets up
        self.layout.takeAt(self.layout.count() - 1)
        # Add the next widget
        self.layout.addWidget(view)
        # Add the spacer back to prop widgets up
        self.layout.addStretch(1)

    def show_prev(self, view: TTableView):
        raise NotImplementedError()

    @pyqtSlot(TFailure)
    def handle_triggered(self, failure: TFailure):
        raise NotImplementedError()