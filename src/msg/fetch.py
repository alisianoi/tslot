import logging

from src.msg.base import TRequest, TResponse


class TFetchRequest(TRequest):
    """
    Ask the backend to fulfill some read-only request

    This is the base class for different kinds of requests:

    1. Recorded time slot requests
    2. Currently active timer requests
    3. Task/Project/Tag autocompletion requests
    4. etc

    For writing to the backend, see TStoreRequest.
    """

    def __init__(self):
        pass


class TFetchResponse(TResponse):
    """
    Ask the frontend to process some response

    This is the base class for different kinds of responses:

    1. Respond with a list of recorded time slots
    2. Respond with a list of currently active timers
    3. Respond with a list of autocompletion suggestsions
    4. etc

    This is expected to be a reply to some previous request, see
    subclasses of TFetchRequest.
    """

    def __init__(self):
        pass
