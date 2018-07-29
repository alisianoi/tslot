import logging


class TMessage:
    """Base class for all messages"""

    def __init__(self):

        self.logger = logging.getLogger('tslot')

    def key_val_or_key_len(self, key, val):
        """Help show (reasonably truncated) key/value pairs to a human"""

        if isinstance(val, list) and len(val) > 3:
            return f'len({key})={len(val)}'
        if isinstance(val, dict) and len(val) > 3:
            return f'len({key})={len(val)}'

        return f'{key}={val}'

    def __repr__(self):
        args = ', '.join(
            self.key_val_or_key_len(key, val)
            for key, val in self.__dict__.items()
        )

        return self.__class__.__name__ + '(' + args + ')'

class TFailure(TMessage):
    """Base class for all failure messages"""

    def __init__(self, message):

        self.message = message

class TRequest(TMessage):
    """Base class for all requests"""

    pass

class TResponse(TMessage):
    """Base class for all responses"""

    pass
