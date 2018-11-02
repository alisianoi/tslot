from typing import List

from src.ai.model import TEntryModel
from src.msg.stash import TStashResponse


class TEntryStashResponse(TStashResponse):

    def __init__(self, items: List[TEntryModel]):

        self.items = items
