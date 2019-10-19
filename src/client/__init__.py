from multiprocessing.queues import Queue

from PyQt5.QtWidgets import QApplication

from src.client.wgt_main import TMainWindow


class Client:
    def __init__(self, incoming_messages: Queue, outgoing_messages: Queue):
        self.incoming_messages = incoming_messages
        self.outgoing_messages = outgoing_messages

    def start(self):
        print("client: here we go")
        app = QApplication(sys.argv)

        main_window = TMainWindow()
        main_window.show()

        return app.exec()


def client(incoming_messages: Queue, outgoing_messages: Queue):
    return Client(incoming_messages, outgoing_messages).start()
