from typing import List

from src.common.response.fetch import TFetchResponse
from src.db.model import TagModel


class TTagFetchResponse(TFetchResponse):

    def __init__(self, tags: List[TagModel]):

        self.tags = tags


class TTagsByNameFetchResponse(TTagFetchResponse):

    def __init__(self, tags: List[TagModel]):

        super().__init__(tags=tags)
