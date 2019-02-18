import pendulum

from pendulum import Date
from pendulum.tz.timezone import Timezone

from typing import List, Tuple

from src.common.dto.fetch import TFetchResponse
from src.common.dto.slot_fetch_request import TRaySlotFetchRequest, TRaySlotWithTagFetchRequest

from src.ai.model import TEntryModel


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

    TODO: think why there is no super call/think about architecture
    """

    def __init__(
        self
        , items: List[TEntryModel]
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

    def is_empty(self) -> bool:
        return True if not self.items else False

    def in_timezone(self, tz: Timezone=pendulum.local_timezone()):
        """
        Convert all the time slots into the supplied timezone

        :param tz: the supplied timezone
        """

        for i, item in enumerate(self.items):
            slot = item.slot

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

    def break_by_date(self) -> List[Tuple[int, int]]:
        """Regroup the supplied list of time slots by date"""

        i, j = 0, 0
        result = []

        while i != len(self.items):
            fst_slot = self.items[i].slot

            while j != len(self.items):
                lst_slot = self.items[j].slot

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
    """

    def __init__(
        self
        , items: List[TEntryModel]
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

    @classmethod
    def from_params(
        cls
        , items: List[TEntryModel]
        , dt_offset: Date
        , direction: str
        , dates_dir: str
        , times_dir: str
        , slice_fst: int
        , slice_lst: int
    ):
        return cls(
            items
            , dt_offset
            , direction
            , dates_dir
            , times_dir
            , slice_fst
            , slice_lst
        )

    @classmethod
    def from_request(
        cls
        , items: List[TEntryModel]
        , request: TRaySlotFetchRequest
    ):
        return cls(
            items
            , request.dt_offset
            , request.direction
            , request.dates_dir
            , request.times_dir
            , request.slice_fst
            , request.slice_lst
        )


class TRaySlotWithTagFetchResponse(TSlotFetchResponse):
    """Return time slots for a ray slot fetch with tags request"""

    def __init__(
        self
        , items: List[TEntryModel]
        , dt_offset: Date
        , direction: str
        , dates_dir: str
        , times_dir: str
        , flat_tags: bool
        , slice_fst: int
        , slice_lst: int
    ) -> None:

        self.dt_offset = dt_offset
        self.direction = direction
        self.flat_tags = flat_tags

        super().__init__(items, dates_dir, times_dir, slice_fst, slice_lst)

        if not self.flat_tags:
            self.condense_tags()

    def in_timezone(self, tz: Timezone=pendulum.local_timezone()):
        """
        Convert all the time slots into the supplied timezone

        :param tz: the supplied timezone
        """

        self.dt_offset = self.dt_offset.in_timezone(tz)

        super().in_timezone(tz)

    @classmethod
    def from_params(
        cls
        , items: List[TEntryModel]
        , dt_offset: Date
        , direction: str
        , dates_dir: str
        , times_dir: str
        , flat_tags: bool
        , slice_fst: int
        , slice_lst: int
    ):

        return cls(
            items
            , dt_offset
            , direction
            , dates_dir
            , times_dir
            , flat_tags
            , slice_fst
            , slice_lst
        )

    @classmethod
    def from_request(
        cls
        , items: List[TEntryModel]
        , request: TRaySlotWithTagFetchRequest
    ):

        return cls(
            items
            , request.dt_offset
            , request.direction
            , request.dates_dir
            , request.times_dir
            , request.flat_tags
            , request.slice_fst
            , request.slice_lst
        )

    def condense_tags(self):
        """
        Condense all the tags that belong to the same task into one list

        By default the list of items that come from the database has this form:
        [TEntryModel(slot0, task0, [tag0]), TEntryModel(slot0, task0, [tag1])]

        After `condense_tags`, the tags should become condensed like so:
        [TEntryModel(slot0, task0, [tag0, tag1])]
        """

        fst, lst = 0, 1

        items, self.items = self.items, []

        while fst != len(items):

            lst = self.find_next_entry(items, fst)

            self.check_entry_segment(items, fst, lst)

            self.items.append(
                TEntryModel(
                    items[fst].slot
                    , items[fst].task
                    , [tag for item in items[fst : lst] for tag in item.tags]
                )
            )

            fst = lst

    def find_next_entry(self, items: List[TEntryModel], fst: int) -> int:
        """Find the next entry with a different task or slot"""

        if not (0 <= fst and fst < len(items)):
            raise RuntimeError('Expecting index to be within [0, len(items))')

        for i in range(fst, len(items)):
            if items[i].slot != items[fst].slot:
                return i

        return len(items)

    def check_entry_segment(
        self
        , items: List[TEntryModel]
        , fst: int
        , lst: int
    ) -> None:
        """
        Check that the segments meets certain expectations

        1. All the elements should belong to the same slot and task
        2. All the tags should be distinct and one (or none) tag per entry
        """

        tags = []

        for i in range(fst, lst):
            if items[i].slot != items[fst].slot:
                raise RuntimeError('Expecting all slots to be equal')
            if items[i].task != items[fst].task:
                raise RuntimeError('Expecting all tasks to be equal')
            if len(items[i].tags) > 1:
                raise RuntimeError('Expecting no more than one tag per entry')

            tags.extend(items[i].tags)

        tags.sort()

        for i in range(1, len(tags)):
            if tags[i] == tags[i - 1]:
                raise RuntimeError('Expecting no tag duplicates')

        # All checks have passed
