from PyQt5.QtCore import *

from src.common.dto.model import TEntryModel
from src.common.dto.fetch import TFetchRequest, TFetchResponse
from src.common.dto.stash import TStashRequest, TStashResponse


class TTimerStashRequest(TStashRequest):

    def __init__(self, data: TEntryModel):

        self.tdata = data

class TTimerStashResponse(TStashResponse):

    pass
