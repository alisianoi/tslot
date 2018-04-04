import logging

class TFailure:

    def __init__(self, message):

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

        self.message = message

        self.logger.debug(self)

    def __repr__(self):
        return f'TFailure(message={self.message})'

class TRequest:

    def __init__(self):

        self.name = self.__class__.__name__
        self.logger = logging.getLogger('tslot')

class TResponse:

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

