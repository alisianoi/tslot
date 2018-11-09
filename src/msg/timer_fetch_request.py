from src.ai.model import TEntryModel
from src.msg.fetch import TFetchRequest, TFetchResponse


class TTimerFetchRequest(TFetchRequest):
    """Request a currently active timer"""

    pass


class TTimerFetchResponse(TFetchResponse):
    """Respond with a currently active timer (or empty)"""

    def __init__(self, timer: TEntryModel=None) -> None:

        self.timer = timer
