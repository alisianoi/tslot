from src.msg.fetch import TFetchRequest, TFetchResponse


class TTagFetchRequest(TFetchRequest):

    def __init__(self, tasks: list) -> None:

        self.tasks = tasks

class TTagFetchResponse(TFetchResponse):

    def __init__(self, tags: list) -> None:

        self.tags = tags
