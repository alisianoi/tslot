from multiprocessing.queues import Queue

from src.common.request.fetch.slot_fetch_request import TRaySlotFetchRequest
from src.common.request.fetch.slot_fetch_request import TRaySlotWithTagFetchRequest  # NOQA
from src.common.request.fetch.slot_fetch_request import TSlotFetchRequest
from src.server.service.slot_service import TSlotService


class TSlotController:
    def __init__(self, outgoing_messages: Queue):
        self.outgoing_messages = outgoing_messages

        self.service = TSlotService()

    def fetch(self, request: TSlotFetchRequest):
        if isinstance(request, TRaySlotFetchRequest):
            self.outgoing_messages.put(self.service.fetch_ray_slot(request))
        elif isinstance(request, TRaySlotWithTagFetchRequest):
            self.outgoing_messages.put(service.fetch_ray_slot_with_tag(request))
        else:
            raise RuntimeError(f"{__class__.__name__} failed to identify request")
