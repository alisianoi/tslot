from src.common.dto.model import TEntryModel
from src.common.response.fetch import TFetchResponse


class TTimerFetchResponse(TFetchResponse):
    """Respond with a currently active timer (or empty)"""

    def __init__(self, timer: TEntryModel = None) -> None:
        self.timer = timer
