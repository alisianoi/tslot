import pendulum

from typing import List

from pendulum import DateTime
from pendulum.tz.timezone import Timezone


from src.db.model import SlotModel, TaskModel, TagModel

# Q: Why do these models (almost) replicate the ones from src/db/models.py?
# A: Currently, connecting to the database works roughly like this:
#    1. A specific reader or writer instance is tasked with a request
#    2. It opens a brand-new session to connect to the database
#    3. The result of the request are instances from src/db/models.py
#    4. The reader or writer closes their session
#
#    Once the session is closed, instances of src/db/models.py no longer work,
#    so it is necessary to copy the data from them out into the instances below.
#
#    Also, some classes here (e.g. TEntryModel) have no direct corresponding
#    instance in src/db/models.py because they are a higher-level data unit.
#
#    Finally, it would be possible to make all workers use the same session and
#    never close that session. This would require explicit syncronization for
#    that session and remove *some* duplicating classes from here.
#
# Q: Why do classes have `from_xxx` methods that are the same as `__init__`?
# A: Just for symmetry. The `from_xxx` methods exist because the instances are
#    created by both the database layer (and then using the database model is
#    convenient) and by the GUI layer (and then using separate parameters is
#    convenient).


class TTagModel:
    def __init__(self, name: str, id: int = None) -> None:

        self.id, self.name = id, name

    @classmethod
    def from_params(cls, name: str = None, id: int = None):
        return cls(name, id)

    @classmethod
    def from_model(cls, model: SlotModel):
        return cls(model.name, model.id)

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
            raise RuntimeError("Must compare against another tag model")

        if self.name < other.name:
            return True

        return False

    def __le__(self, other):

        if not isinstance(other, TTagModel):
            raise RuntimeError("Must compare against another tag model")

        if self.name <= other.name:
            return True

        return False


class TTaskModel:
    """
    Represent a task that the user is doing/has done.

    The name is optional because the timer could be started on a blank task.
    """

    def __init__(self, name: str = None, id: int = None) -> None:

        self.id, self.name = id, name

    @classmethod
    def from_params(cls, name: str = None, id: int = None):
        return cls(name, id)

    @classmethod
    def from_model(cls, model: TaskModel):
        return cls(model.name, model.id)

    def __eq__(self, other):

        if not isinstance(other, TTaskModel):
            return False

        if self.id != other.id:
            return False
        if self.name != other.name:
            return False

        return True

    def __lt__(self, other):

        if not isinstance(other, TTaskModel):
            raise RuntimeError("Must compare against another task model")

        if self.name < other.name:
            return True

        return False

    def __le__(self, other):

        if not isinstance(other, TTaskModel):
            raise RuntimeError("Must compare against another task model")

        if self.name <= other.name:
            return True

        return False


class TSlotModel:
    """
    Represents a time interval between first and last time points.

    The first time point must be known but the last time point might not be.
    Accepts the time points in whatever time zone they might be, then converts
    them to UTC.
    """

    def __init__(self, fst: DateTime, lst: DateTime = None, id: int = None):

        name = self.__class__.__name__

        if not isinstance(fst, DateTime):
            raise TypeError(f"{name} expects `fst` to be DateTime")

        self.id = id
        self.fst = fst
        self.lst = lst

        self.in_timezone()

        if self.lst is None:
            return

        if not isinstance(lst, DateTime):
            raise TypeError(f"{name} expects `lst` to be DateTime")
        if self.lst <= self.fst:
            raise ValueError(f"{name} expects `fst` to be earlier than `lst`")

    def in_timezone(self, tz: Timezone = pendulum.tz.UTC):

        self.fst = self.fst.in_timezone(tz)

        if self.lst:
            self.lst = self.lst.in_timezone(tz)

    @classmethod
    def from_params(cls, fst: DateTime, lst: DateTime = None, id: int = None):
        return cls(fst, lst, id)

    @classmethod
    def from_model(cls, model: SlotModel):
        fst, lst = pendulum.instance(model.fst).in_timezone("UTC"), None

        if model.lst is not None:
            lst = pendulum.instance(model.lst).in_timezone("UTC")

        return cls(fst, lst, model.id)

    def __eq__(self, other):

        if not isinstance(other, TSlotModel):
            raise RuntimeError("Must compare against another slot model")

        if self.id != other.id:
            return False
        if self.fst != other.fst:
            return False
        if self.lst != other.lst:
            return False

        return True


class TEntryModel:
    """Holds together a slot model, a task model and its corresponding tags."""

    def __init__(
        self,
        slot: TSlotModel,
        task: TTaskModel = TTaskModel(),
        tags: List[TTagModel] = None,
    ) -> None:

        self.slot = slot
        self.task = task
        self.tags = [] if tags is None else tags

    def __repr__(self) -> str:
        return f"{self.task.name}: {self.slot.fst} -- {self.slot.lst}"
