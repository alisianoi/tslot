import pendulum

from pendulum import Date, Timezone

from src.msg.fetch import TFetchRequest, TFetchResponse


LOAD_DIRECTIONS = ['past_to_future', 'future_to_past']


class TSlotFetchRequest(TFetchRequest):
    """
    Ask for previously recorded time slots

    The returned list of time slots can be sorted in many ways:

    a) by date
    b) by time within the same date

    There could also be many time slots, so ask to slice the
    list and return only the slots in [slice_fst, slice_lst).

    :param dates_dir: sort dates from past to future or vice versa
    :param times_dir: sort times from past to future or vice versa
    :param slice_fst: the index of the first slot to return
    :param slice_lst: the index of the first slot *not* to return
    """

    def __init__(
        self
        , dates_dir: str='past_to_future'
        , times_dir: str='past_to_future'
        , slice_fst: int=0
        , slice_lst: int=128
    ):

        super().__init__()

        msg = 'Expected {} from {}, was {}'

        if dates_dir not in LOAD_DIRECTIONS:
            raise RuntimeError(
                msg.format('dates_dir', LOAD_DIRECTIONS, dates_dir)
            )

        if times_dir not in LOAD_DIRECTIONS:
            raise RuntimeError(
                msg.format('times_dir', LOAD_DIRECTIONS, times_dir)
            )

        if slice_fst > slice_lst:
            raise RuntimeError(
                'Expected slice_fst <= slice_lst, but was >'
            )

        self.dates_dir = dates_dir
        self.times_dir = times_dir
        self.slice_fst = slice_fst
        self.slice_lst = slice_lst


class TRaySlotFetchRequest(TSlotFetchRequest):
    """
    Ask for recorded time slots before (after) a datetime offset

    If the datetime offset splits some time slot, it is returned
    together with the other results. The datetime offset could be
    chosen so that no time slots are returned as a result.

    The datetime offset together with direction are the required
    parameters to uniquely identify the ray. If direction equals
    future to past, then the ray begins at the datetime offset and
    continues into the future. If direction equals past to future,
    then the ray begins at some point in the past and ends at the
    datetime offset.

    :param dt_offset: the datetime offset
    :param direction: the direction of the ray
    :param dates_dir: sort dates from past to future or vice versa
    :param times_dir: sort times from past to future or vice versa
    :param slice_fst: the index of the first slot to return
    :param slice_lst: the index of the first slot *not* to return
    """

    def __init__(
        self
        , dt_offset: Date=pendulum.today()
        , direction: str='future_to_past'
        , dates_dir: str='future_to_past'
        , times_dir: str='past_to_future'
        , slice_fst: int=0
        , slice_lst: int=128
    ):

        super().__init__(dates_dir, times_dir, slice_fst, slice_lst)

        if direction not in LOAD_DIRECTIONS:
            raise RuntimeError(f'Expected direction from {LOAD_DIRECTION}, was {direction}')

        self.dt_offset = dt_offset
        self.direction = direction


class TRaySlotWithTagFetchRequest(TSlotFetchRequest):
    """
    Ask for recorded time slots before (after) a datetime offset

    The time slots are returned together with their assigned tags.

    See TRaySlotFetchRequest

    :param flat_tags: TODO: what is flat tags?
    """

    def __init__(
        self
        , dt_offset: Date=pendulum.today()
        , direction: str='future_to_past'
        , dates_dir: str='future_to_past'
        , times_dir: str='past_to_future'
        , flat_tags: bool=False
        , slice_fst: int=0
        , slice_lst: int=128
    ) -> None:

        super().__init__(dates_dir, times_dir, slice_fst, slice_lst)

        if direction not in LOAD_DIRECTIONS:
            raise RuntimeError(f'Expected direction from {LOAD_DIRECTION}, was {direction}')

        self.dt_offset = dt_offset
        self.direction = direction
        self.flat_tags = flat_tags


class TSlotFetchResponse(TFetchResponse):
    """
    Present a list of time slots as response to some request

    This class acts as a base class for several response classes.

    :param items: the list of time slots
    :param request: the original request to fetch time slots
    """

    def __init__(self, items: list, request: TSlotFetchRequest):

        super().__init__(items, request)

        # Convert from UTC+00:00 to local timezone
        self.in_timezone(tz=pendulum.local_timezone())

    def in_timezone(self, tz: Timezone=pendulum.local_timezone()):

        self.dt_offset = self.dt_offset.in_timezone(tz)

        for i, item in enumerate(self.items):
            slot = item[0]

            slot.fst = pendulum.instance(slot.fst).in_timezone(tz)
            slot.lst = pendulum.instance(slot.lst).in_timezone(tz)

            self.items[i] = item

    def in_direction(self, direction: str='past_to_future'):

        # Direction is given with respect to the datetime offset
        # Changing direction means you must make another request
        raise RuntimeError('Cannot change direction')

    def in_times_dir(self, times_dir: str='past_to_future'):

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
    """Return time slots for a ray slot fetch request"""

    def __init__(self, items: list, request: TRaySlotFetchRequest):

        super().__init__(items, request)


class TRaySlotWithTagFetchResponse(TSlotFetchResponse):
    """Return time slots for a ray slot fetch with tags request"""

    def __init__(self, items: list, request: TRaySlotWithTagFetchRequest):

        super().__init__(items, request)

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
