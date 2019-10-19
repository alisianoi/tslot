import pendulum

from pendulum import Date

from src.common.request.fetch import TFetchRequest


LOAD_DIRECTIONS = ["past_to_future", "future_to_past"]


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
        self,
        dates_dir: str = "past_to_future",
        times_dir: str = "past_to_future",
        slice_fst: int = 0,
        slice_lst: int = 128,
    ) -> None:

        if dates_dir not in LOAD_DIRECTIONS:
            raise RuntimeError(
                f"Expected dates_dir from {LOAD_DIRECTIONS}, was {dates_dir}"
            )

        if times_dir not in LOAD_DIRECTIONS:
            raise RuntimeError(
                f"Expected times_dir from {LOAD_DIRECTIONS}, was {times_dir}"
            )

        if slice_fst > slice_lst:
            raise RuntimeError("Expected slice_fst <= slice_lst, but was >")

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
        self,
        dt_offset: Date = pendulum.today(),
        direction: str = "future_to_past",
        dates_dir: str = "future_to_past",
        times_dir: str = "past_to_future",
        slice_fst: int = 0,
        slice_lst: int = 128,
    ) -> None:

        super().__init__(dates_dir, times_dir, slice_fst, slice_lst)

        if direction not in LOAD_DIRECTIONS:
            raise RuntimeError(
                f"Expected direction from {LOAD_DIRECTION}, was {direction}"
            )

        self.dt_offset = dt_offset
        self.direction = direction


class TRaySlotWithTagFetchRequest(TSlotFetchRequest):
    """
    Ask for recorded time slots before (after) a datetime offset

    The time slots are returned together with their assigned
    tags. Each slot could have several tags simultaneously. In a
    relational database that is represented with a table where each
    row holds a slot followed by one of its tags. So, the slots are
    duplicated. Instead of this, you could instruct the Python code
    to flatten out the tags and remove the duplication.

    Example (flat tags):
    [['slot0', ['tag0', 'tag1']], ['slot1', ['tag2']]]

    Example (non-flat tags):
    [['slot0', 'tag0'], ['slot0', 'tag1'], ['slot1', 'tag2']]

    See :class TRaySlotFetchRequest:

    :param flat_tags: flatten the tags of each slot into a list
    """

    def __init__(
        self,
        dt_offset: Date = pendulum.today(),
        direction: str = "future_to_past",
        dates_dir: str = "future_to_past",
        times_dir: str = "past_to_future",
        flat_tags: bool = False,
        slice_fst: int = 0,
        slice_lst: int = 128,
    ) -> None:

        super().__init__(dates_dir, times_dir, slice_fst, slice_lst)

        if direction not in LOAD_DIRECTIONS:
            raise RuntimeError(
                f"Expected direction from {LOAD_DIRECTION}, was {direction}"
            )

        self.dt_offset = dt_offset
        self.direction = direction
        self.flat_tags = flat_tags
