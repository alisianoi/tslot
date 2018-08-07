from PyQt5.QtCore import *

from src.db.model import SlotModel
from src.msg.fetch import TFetchRequest, TFetchResponse


class TTimerRequest(TFetchRequest):
    """Request a currently active timer"""

    pass


class TTimerResponse(TFetchResponse):
    """Respond with a currently active timer (or empty)"""

    def __init__(self, items: SlotModel=None) -> None:

        self.items = items
