from typing import List

from pendulum import DateTime


class TTagModel:

    def __init__(self, name: str, id: int=None) -> None:

        self.id = id
        self.name = name


class TTaskModel:

    def __init__(self, name: str, id: int=None) -> None:

        self.id = id
        self.name = name


class TSlotModel:

    def __init__(self, fst: DateTime, lst: DateTime=None, id: int=None) -> None:

        self.id = id
        self.fst = fst
        self.lst = lst


class TEntryModel:

    def __init__(
        self
        , slot: TSlotModel
        , task: TTaskModel=None
        , tags: List[TTagModel]=None
    ) -> None:

        self.slot = slot
        self.task = task
        self.tags = [] if tags is None else tags
