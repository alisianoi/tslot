from src.common import TMessage


class TFailure(TMessage, Exception):
    """Base class for all failure messages"""

    def __init__(self, message):
        super().__init__(message)

        self.message = message
