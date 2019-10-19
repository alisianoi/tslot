from src.common.dto.model import TEntryModel
from src.common.request.stash import TStashRequest


class TTimerStashRequest(TStashRequest):
    def __init__(self, data: TEntryModel):
        self.tdata = data
