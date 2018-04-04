import pendulum

from src.msg.fetch import TFetchRequest, TFetchResponse


LOAD_DIRECTIONS = ['future_to_past', 'past_to_future']


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
        , dt_offset: pendulum.date=pendulum.today()
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
        tz = pendulum.local_timezone()

        for i, item in enumerate(self.items):
            slot, task = item

            slot.fst = pendulum.instance(slot.fst).in_timezone(tz)
            slot.lst = pendulum.instance(slot.lst).in_timezone(tz)

            self.items[i] = (slot, task)
