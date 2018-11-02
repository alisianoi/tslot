from typing import List

from src.ai.model import TEntryModel
from src.msg.stash import TStashRequest


class TEntryStashRequest(TStashRequest):

    def __init__(self, items: List[TEntryModel]):

        self.items = items
