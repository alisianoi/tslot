from multiprocessing import Pool, Process, Queue

from src.common.request.fetch.slot_fetch_request import TSlotFetchRequest
from src.server.controller.slot_controller import TSlotController


class Server:
    def __init__(self, incoming_messages: Queue, outgoing_messages: Queue):

        self.pool = Pool()

        self.incoming_messages = incoming_messages
        self.outgoing_messages = outgoing_messages

        self.timer_controller = TTimerController()
        self.slot_controller = TSlotController()
        self.tag_controller = TTagController()

    def start(self):
        while True:
            try:
                request = self.incoming_messages.get()
            except Exception as exception:
                break

            if isinstance(request, TSlotFetchRequest):
                self.handle_slot_fetch_request(request)
            elif isinstance(message, TagRequest):
                self.handle_tag_request(message)
            else:
                raise RuntimeError("Failed to recognize message")

    def handle_slot_request(self, request: TSlotFetchRequest):
        self.pool.apply_async(func=self.slot_controller.fetch, args=(request))

    def handle_success(self, response):
        self.outgoing_messages.put(response)

    def handle_failure(self, response):
        print(f"handle failure: {response}")


def server(incoming_messages: Queue, outgoing_messages: Queue):
    return Server(incoming_messages, outgoing_messages).start()
