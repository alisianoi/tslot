class TFailure:
    '''Show that something went wrong'''

class TFetchRequest:
    '''Base class for all types of requests, like LoadRequestRay'''

class TSlotFetchRequest(TFetchRequest):
    '''Base class for all types of Slot loading requests'''

class TSegmentSlotFetchRequest(TSlotFetchRequest):
    '''Load a segment of slots'''

class TRaySlotFetchRequest(TSlotFetchRequest):
    '''Load a ray of slots'''

class TTagFetchRequest(TFetchRequest):
    '''Base class for all types of Tag loading requests'''

class TFetchResponse:
    '''Response with the actually loaded data, like LoadResponseRay'''

class TStashRequest:
    '''Basse class for all types of write requests, like StoreRequestSlot'''

class TCompleteRequest:
    '''???'''

class TWorker:

    started = pyqtSignal()
    stopped = pyqtSignal()

    alerted = pyqtSignal(TFailure)

    def work(self):
        pass # Subclasses must implement this


class TReader(TWorker):

    fetched = pyqtSignal(TFetchResponse)

    def __init__(self, request: TFetchRequest)

    def work(self):
        pass


class TWriter(TWorker):

    stashed = pyqtSignal(TStashResponse)

    def __init__(self, request: TStashRequest):
        pass

    def work(self):
        pass


class TDiskBroker:

    responsed = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    @pyqtSlot(TRequest)
    def handle_requested(self, request: TRequest):
        # Connected upstream to TDiskCache.requested
        pass

    @pyqtSlot(TFetchResponse)
    def handle_fetched(self, response: TFetchResponse):
        # Connected downstream to TReader.fetched
        pass

    @pyqtSlot(TStashResponse)
    def handle_stashed(self, response: TStashResponse):
        # Connected downstream to TWriter.stashed
        pass

    @pyqtSlot(TFailure)
    def handle_alerted(self, failure: TFailure):
        # Connected downstream to TWorker.alerted
        pass


class TCacheBroker:

    requested = pyqtSignal(TRequest)
    responded = pyqtSignal(TResponse)
    triggered = pyqtSignal(TFailure)

    @pyqtSlot(TRequest):
    def handle_requested(self, request: TRequest):
        # Connected upstream to TWidget.requested
        pass

    @pyqtSlot(TResponse)
    def handle_responded(self, response: TResponse):
        # Connected downstream to TDiskBroker.responded
        pass

    @pyqtSlot(Failure)
    def handle_triggered(self, failure: Failure):
        # Connected downstream to TDiskBroker.triggered
        pass

class TWidget0:

    requested = pyqtSignal(TRequest)

    @pyqtSlot(TResponse)
    def handle_responded(self, response: TResponse):
        pass

    @pyqtSlot(TFailure)
    def handle_triggered(self, failure: TFailure):
        pass

class TWidget1:

    requested = pyqtSignal(TRequest)

    @pyqtSlot(TResponse)
    def handle_responsed(self, response: TResponse):
        pass

    @pyqtSlot(TFailure)
    def handle_triggered(self, failure: TFailure):
        pass
