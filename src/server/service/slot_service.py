from src.common.request.fetch.slot_fetch_request import TRaySlotFetchRequest
from src.common.request.fetch.slot_fetch_request import TRaySlotWithTagFetchRequest
from src.server.repository.slot_repository import TSlotRepository


class TSlotService:
    def __init__(self):
        self.repository = TSlotRepository()

    def fetch_ray_slot(self, request: TRaySlotFetchRequest):
        return self.repository.fetch_ray_slot(request)

    def fetch_ray_slot_with_tag(self, request: TRaySlotWithTagFetchRequest):
        return self.repository.fetch_ray_slot_with_tag(request)
