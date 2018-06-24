import logging

from src.msg.base import TRequest, TResponse

LOAD_DIRECTIONS = ['past_to_future', 'future_to_past']


class TFetchRequest(TRequest):
    '''
    Base class for different data fetching requests

    :param slice_fst: the first item to include
    :param slice_lst: the first item to exclude
    '''

    def __init__(self, slice_fst: int=0, slice_lst: int=128):

        if slice_fst > slice_lst:
            raise RuntimeError(
                'Expected slice_fst to be <= than slice_lst'
            )

        self.slice_fst = slice_fst
        self.slice_lst = slice_lst

class TFetchResponse(TResponse):
    '''
    Base class for different data fetching responses

    :param items:   the fetched items
    :param request: the original request
    '''

    def __init__(self, items: list, request: TFetchRequest):

        super().__init__(request)

        self.items = items

    def is_empty(self) -> bool:
        return False if self.items else True
