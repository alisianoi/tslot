from typing import List

from pendulum import Date


class TTagModel:

    def __init__(self, name: str, id: int=None) -> None:

        self.id = id
        self.name = name


class TTaskModel:

    def __init__(self, name: str, id: int=None) -> None:

        self.id = id
        self.name = name


class TSlotModel:

    def __init__(self, fst: Date, lst: Date=None, id: int=None) -> None:

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
