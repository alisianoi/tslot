import logging


class TMessage:
    """
    Base class for all messages

    Messages are an integral part of the request-response-trigger protocol.
    TODO: link to documentation

    Messages are passed primarily between graphical widgets and backend
    services. For example, a widget could issue a request to fetch time slots.
    The request message would be received by a backend service that would
    eventually ask the database for the required data.
    """

    def __init__(self):

        self.logger = logging.getLogger("tslot-main")

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