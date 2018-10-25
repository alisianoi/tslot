from src.msg.fetch import TFetchRequest


class TTagFetchRequest(TFetchRequest):

    pass


class TTagsByNameFetchRequest(TTagFetchRequest):

    def __init__(self, name: str, exact: bool=False) -> None:

        self.name, self.exact = name, exact
