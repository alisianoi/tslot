from typing import List

from src.db.model import TagModel
from src.common.dto.fetch import TFetchResponse


class TTagFetchResponse(TFetchResponse):

    def __init__(self, tags: List[TagModel]):

        self.tags = tags


class TTagsByNameFetchResponse(TTagFetchResponse):

    def __init__(self, tags: List[TagModel]):

        super().__init__(tags=tags)
