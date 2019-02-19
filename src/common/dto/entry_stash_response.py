from typing import List

from src.common.dto.model import TEntryModel
from src.common.dto.stash import TStashResponse


class TEntryStashResponse(TStashResponse):

    def __init__(self, items: List[TEntryModel]):

        self.items = items
