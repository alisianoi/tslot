from src.common.request import TRequest


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
