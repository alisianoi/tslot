from PyQt5.QtCore import QObject, QThreadPool


class TTimerService(QObject):

    loaded = pyqtSignal(TResponse)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.threadpool = QThreadPool.globalInstance()

    def fetch_timer(self):
        pass
