from typing import List

from pendulum import DateTime

from src.db.model import SlotModel, TaskModel, TagModel


class TTagModel:

    def __init__(self, model: SlotModel) -> None:

        self.id, self.name = model.id, model.name

    def __eq__(self, other):

        if not isinstance(other, TTagModel):
            return False

        if self.id != other.id:
            return False
        if self.name != other.name:
            return False

        return True

    def __lt__(self, other):

        if not isinstance(other, TTagModel):
            raise RuntimeError('Expecting comparison against another tag model')

        if self.id == other.id:
            return False
        if self.name < other.name:
            return True

        return False

    def __le__(self, other):

        if not isinstance(other, TTagModel):
            raise RuntimeError('Expecting comparison against another tag model')

        if self.id == other.id:
            return True
        if self.name <= other.name:
            return True

        return False


class TTaskModel:

    def __init__(self, model: TaskModel) -> None:

        self.id, self.name = model.id, model.name

    def __eq__(self, other):

        if not isinstance(other, TTaskModel):
            return False

        if self.id != other.id:
            return False
        if self.name != other.name:
            return False

        return True


class TSlotModel:

    def __init__(self, model: SlotModel) -> None:

        self.id, self.fst, self.lst = model.id, model.fst, model.lst

    def __eq__(self, other):

        if not isinstance(other, TSlotModel):
            return False

        if self.id != other.id:
            return False
        if self.fst != other.fst:
            return False
        if self.lst != other.lst:
            return False

        return True


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
