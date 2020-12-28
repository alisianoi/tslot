from src.common.request.fetch import TFetchRequest


class TTagFetchRequest(TFetchRequest):
    pass


class TTagsByNameFetchRequest(TTagFetchRequest):
    def __init__(self, name: str):
        super().__init__()

        self.name = name
