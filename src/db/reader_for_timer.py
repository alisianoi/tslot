from pathlib import Path

from src.ai.base import TObject

from src.db.model import SlotModel
from src.db.worker import TReader
from src.msg.timer import TTimerRequest, TTimerResponse

class TTimerReader(TReader):

    def __init__(
        self
        , request: TTimerRequest
        , path   : Path=None
        , parent : TObject=None
    ) -> None:
        super().__init__(request, path, parent)

    def work(self) -> None:

        if self.session is None:
            self.session = self.create_session()

        items = self.session.query(
            SlotModel
        ).filter(
            SlotModel.lst is None
        ).all()

        if len(items) != 0 and len(items) != 1:
            raise RuntimeError("There should be 0 or 1 active timer")

        self.fetched.emit(TTimerResponse(items))

        self.session.close()
