from src.common.request.fetch import TFetchRequest


class TTagFetchRequest(TFetchRequest):

    pass


class TTagsByNameFetchRequest(TTagFetchRequest):
    def __init__(self, name: str, exact: bool = False):
        self.name, self.exact = name, exact
