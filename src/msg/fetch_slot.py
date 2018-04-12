import pendulum

from pendulum import Date, Timezone

from src.msg.fetch import TFetchRequest, TFetchResponse


LOAD_DIRECTIONS = ['past_to_future', 'future_to_past']


class TSlotFetchRequest(TFetchRequest):

    def __init__(
        self
        , dates_dir: str='past_to_future'
        , times_dir: str='past_to_future'
        , slice_fst: int=0
        , slice_lst: int=128
    ):

        super().__init__(slice_fst, slice_lst)

        msg = 'Expected {} from {}, was {}'

        if dates_dir not in LOAD_DIRECTIONS:
            raise RuntimeError(
                msg.format('dates_dir', LOAD_DIRECTIONS, dates_dir)
            )

        if times_dir not in LOAD_DIRECTIONS:
            raise RuntimeError(
                msg.format('times_dir', LOAD_DIRECTIONS, times_dir)
            )

        self.dates_dir = dates_dir
        self.times_dir = times_dir


class TRaySlotFetchRequest(TSlotFetchRequest):

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


class TRaySlotFetchResponse(TFetchResponse):

    def __init__(self, items: list, request: TRaySlotFetchRequest):

        super().__init__(items, request)

        # Convert from UTC+00:00 to local timezone
        self.in_timezone(tz=pendulum.local_timezone())


    def in_timezone(self, tz: Timezone=pendulum.local_timezone()):

        self.dt_offset = self.dt_offset.in_timezone(tz)

        for i, item in enumerate(self.items):
            slot, task = item

            slot.fst = pendulum.instance(slot.fst).in_timezone(tz)
            slot.lst = pendulum.instance(slot.lst).in_timezone(tz)

            self.items[i] = (slot, task)

    def in_direction(self, direction: str='past_to_future'):

        # Direction is given with respect to the datetime offset
        # If you want to "change" direction, you must make a new request
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
            fst_slot, _ = self.items[i]

            while j != len(self.items):
                lst_slot, _ = self.items[j]

                if fst_slot.fst.date() != lst_slot.fst.date():
                    break

                j += 1

            result.append((i, j))

            i = j

        return result
