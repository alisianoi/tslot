import logging


class TMessage:
    '''
    Base class for all messages
    '''

    def key_val_or_key_len(self, key, val):
        '''
        Return a reasonable key-value string

        If the value is too long, truncate it
        '''

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
    '''
    Base class for all failure messages
    '''

    def __init__(self, message):

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

        self.message = message

        self.logger.debug(self)

class TRequest(TMessage):
    """Base class for all requests"""

    def __init__(self):

        self.logger = logging.getLogger('tslot')


class TResponse(TMessage):
    """Base class for all responses"""

    pass


class TSimpleResponse(TResponse):
    """Base class for all *simple* responses"""

    pass

class TComplexResponse(TResponse):
    """
    Base class for all *complex* responses

    These responses are complex because they also contain the request that is
    being responded to.

    :param request: the original request message
    """

    def __init__(self, request: TRequest):

        self.logger = logging.getLogger('tslot')

        # Copy all parameters from the request into the response
        msg = 'Collision of attribute name {} between {} and {}'

        for key, val in request.__dict__.items():
            if key == 'logger':
                continue

            if key in self.__dict__:
                raise RuntimeError(
                    msg.format(key, self.name, request.name)
                )

            self.__dict__[key] = val
