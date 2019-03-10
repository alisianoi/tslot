from src.common.response import TResponse


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
