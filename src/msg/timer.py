from PyQt5.QtCore import *

from src.ai.model import TEntryModel
from src.msg.fetch import TFetchRequest, TFetchResponse
from src.msg.stash import TStashRequest, TStashResponse


class TTimerRequest(TFetchRequest):
    """Request a currently active timer"""

    pass


class TTimerResponse(TFetchResponse):
    """Respond with a currently active timer (or empty)"""

    def __init__(self, entry: TEntryModel=None) -> None:

        self.entry = entry

class TTimerStashRequest(TStashRequest):

    def __init__(self, data: TEntryModel):

        self.tdata = data

class TTimerStashResponse(TStashResponse):

    pass
