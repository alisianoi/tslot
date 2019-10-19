from typing import List

from src.common.dto.model import TEntryModel
from src.common.request.stash import TStashRequest


class TEntryStashRequest(TStashRequest):
    def __init__(self, items: List[TEntryModel]):
        self.items = items
