from PyQt5.QtCore import *

from src.msg.base import TMessage, TRequest, TResponse


class TTimerRequest(TRequest):

    def __init__(
            self, value: QTime, task: str='', tags: list=None
    ) -> None:

        super().__init__()

        self.value = 


class TTimerResponse(TMessage):

    def __init__(
        self
        , value  : QTime
        , task   : str=''
        , tags   : list=None
        , request: TTimerRequest
    ) -> None:

        super().__init__(request)

        self.task = task
        self.tags = [] if tags is None else tags
