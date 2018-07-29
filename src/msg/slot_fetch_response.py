import pendulum

from pendulum import Date, Timezone

from src.msg.fetch import TFetchResponse
from src.msg.slot_fetch_request import TRaySlotFetchRequest, TRaySlotWithTagFetchRequest


class TSlotFetchResponse(TFetchResponse):
    """
    Return time slots for some time slot request

    This is the base class for several types of responses.

    Args:
        items    : the list of returned time slots
        dates_dir: the direction of dates from the request
        times_dir: the direction of time from the request
        slice_fst: the index of the first element to return
        slice_lst: the index of the first element *not* to return

    TODO: describe the format of :code:`items`
    TODO: think why there is no super call/think about architecture
    """

    def __init__(
        self
        , items: list
        , dates_dir: str
        , times_dir: str
        , slice_fst: int
        , slice_lst: int
    ) -> None:

        self.items = items

        self.dates_dir = dates_dir
        self.times_dir = times_dir
        self.slice_fst = slice_fst
        self.slice_lst = slice_lst

        # Convert from UTC+00:00 to local timezone
        self.in_timezone(tz=pendulum.local_timezone())

    def is_empty(self) -> bool:
        return True if not self.items else False

    def in_timezone(self, tz: Timezone=pendulum.local_timezone()):
        """
        Convert all the time slots into the supplied timezone

        :param tz: the supplied timezone
        """

        for i, item in enumerate(self.items):
            slot = item[0]

            slot.fst = pendulum.instance(slot.fst).in_timezone(tz)
            slot.lst = pendulum.instance(slot.lst).in_timezone(tz)

            self.items[i] = item

    def in_times_dir(self, times_dir: str='past_to_future'):
        """Make the response use the specified times direction"""

        if self.times_dir == times_dir:
            return

        self.reverse_times_dir()

    def reverse_times_dir(self):

        for (fst, lst) in self.break_by_date():
            self.items[fst:lst] = self.items[fst:lst][::-1]

        if self.times_dir == 'past_to_future':
            self.times_dir = 'future_to_past'
        else:
            self.times_dir = 'past_to_future'

    def in_dates_dir(self, dates_dir: str='past_to_future'):
        """Make the response use the specified dates direction"""

        if self.dates_dir == dates_dir:
            return

        self.reverse_dates_dir()

    def reverse_dates_dir(self, reverse_times_dir_too=False):

        self.items = self.items[::-1]

        if reverse_times_dir_too:
            return

        old_times_dir = self.times_dir

        self.reverse_times_dir()

        self.times_dir = old_times_dir

    def break_by_date(self):
        """Regroup the supplied list of time slots by date"""

        i, j = 0, 0
        result = []

        while i != len(self.items):
            fst_slot = self.items[i][0]

            while j != len(self.items):
                lst_slot = self.items[j][0]

                if fst_slot.fst.date() != lst_slot.fst.date():
                    break

                j += 1

            result.append((i, j))

            i = j

        return result


class TRaySlotFetchResponse(TSlotFetchResponse):
    """
    Return time slots for a ray slot fetch request

    The parameters of the original request should be provided as well. These let
    the recipient of this response know how the data from this response could be
    used. Duplicating the request parameters also removes the need to maintain a
    record of requests made by the recipient.

    TODO: describe the format of the elements from :code:`items`
    """

    def __init__(
        self
        , items: list
        , dt_offset: Date
        , direction: str
        , dates_dir: str
        , times_dir: str
        , slice_fst: int
        , slice_lst: int
    ) -> None:

        super().__init__(items, dates_dir, times_dir, slice_fst, slice_lst)

        self.dt_offset = dt_offset
        self.direction = direction

    def in_timezone(self, tz: Timezone=pendulum.local_timezone()):
        """
        Convert all the time slots into the supplied timezone

        :param tz: the supplied timezone
        """

        self.dt_offset = self.dt_offset.in_timezone(tz)

        super().in_timezone(tz)


class TRaySlotWithTagFetchResponse(TSlotFetchResponse):
    """Return time slots for a ray slot fetch with tags request"""

    def __init__(self, items: list, request: TRaySlotWithTagFetchRequest):

        super().__init__(items, request.dates_dir, request.times_dir, request.slice_fst, request.slice_lst)

        self.dt_offset = request.dt_offset
        self.direction = request.direction
        self.flat_tags = request.flat_tags

        if not self.flat_tags:
            self.condense_tags()

    def condense_tags(self):

        i, j = 0, 1

        items, self.items = self.items, []

        while i != len(items):

            slot0, task0, tag0 = items[i]

            tags = [tag0]

            while j != len(items):

                slot1, task1, tag1 = items[j]

                if slot0 != slot1:
                    break

                if task0 != task1:
                    raise RuntimeError('Inconsistency: slots are the same but the tasks are not')

                tags.append(tag1)

                j += 1

            i, j = j, j + 1

            self.items.append((slot0, task0, tags))


class TRaySlotFetchResponseFactory:
    """
    Construct a TRaySlotFetchResponse

    There are at least two ways to get the necessary parameters to construct the
    response. Firstly, the parameters could be coming directly from the request
    (i.e. the original request is known). Secondly, the parameters could have
    been modified or provided directly, in which case the original request could
    not be available.
    """

    @classmethod
    def from_params(
        items: list
        , dt_offset: Date
        , direction: str
        , dates_dir: str
        , times_dir: str
        , slice_fst: int
        , slice_lst: int
    ) -> TRaySlotFetchResponse:

        return TRaySlotFetchResponse(
            items, dt_offset, direction, dates_dir, times_dir, slice_fst, slice_lst
        )

    @classmethod
    def from_request(items: list, request: TRaySlotFetchRequest):

        return TRaySlotFetchRequest(
            items, request.dt_offset, request.direction, request.dates_dir,
            request.times_dir, request.slice_fst, request.slice_lst
        )
