from src.common import TMessage


class TFailure(TMessage):
    """Base class for all failure messages"""

    def __init__(self, message):

        self.message = message
