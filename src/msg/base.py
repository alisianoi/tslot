import logging


class TMessage:

    def key_val_or_key_len(self, key, val):

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

    def __init__(self, message):

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

        self.message = message

        self.logger.debug(self)

class TRequest(TMessage):

    def __init__(self):

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

class TResponse(TMessage):

    def __init__(self, request: TRequest):

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

        # Copy all parameters that the request had into the response
        msg = 'Collision of attribute name {} between {} and {}'

        for key, val in request.__dict__.items():
            if key == 'name':
                continue

            if key in self.__dict__:
                raise RuntimeError(
                    msg.format(key, self.name, request.name)
                )

            self.__dict__[key] = val
