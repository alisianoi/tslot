import logging

from src.msg.base import TRequest, TResponse


class TFetchRequest(TRequest):
    '''
    Provides the base class for all different data fetching requests
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
    Provides the base class for all different data fetching responses
    '''

    def __init__(self, items: list, request: TFetchRequest):

        super().__init__(request)

        self.items = items
