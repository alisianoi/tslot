class TFailure:
    '''Show that something went wrong'''

class TLoadRequest:
    '''Base class for all types of requests, like LoadRequestRay'''

class TLoadResponse:
    '''Response with the actually loaded data, like LoadResponseRay'''

class TStoreRequest:
    '''Basse class for all types of write requests, like StoreRequestSlot'''

class TWorker:

    started = pyqtSignal()
    stopped = pyqtSignal()

    failed = pyqtSignal(Failure)

    def work(self):
        # Subclasses must implement this
        pass

class TReader(TWorker):

    loaded = pyqtSignal(LoadResponse)

    def __init__(self, request: LoadRequest)

    def work(self):
        # Query database, convert to local timezone
        # If anything goes wrong, emit failed
        # Otherwise, emit loaded with the response
        pass

class TWriter(TWorker):

    def __init__(self, request: StoreRequest):
        pass

    def work(self):
        # Convert local timezone to UTC+00:00, write to database
        # If anything goes wrong, emit failed
        # Otherwise, just return
        pass

class TDataBroker:

    loaded = pyqtSignal(LoadResponse)
    failed = pyqtSignal(Failure)

    def __init__(self):
        # Construct a threadpool and prepare to track dispatched workers
        pass

    def load(self, request: LoadRequest):
        # Construct and dispatch a TReader subclass instance
        pass

    def store(self, request: StoreRequest):
        # Construct and dispatch a TWriter subclass instance
        pass

    @pyqtSlot(LoadResponse)
    def handle_loaded(self, response: LoadResponse):
        # Emit loaded
        # Connected to a worker's loaded signal
        pass

    @pyqtSlot(Failure)
    def handle_failed(self, failure: Failure):
        # Maybe silence and retry, maybe emit failed
        # Connected to a worker's failed signal
        pass

class TDataCache:

    loaded = pyqtSignal(LoadResponse)
    failed = pyqtSignal(Failure)

    def __init__(self):
        # Construct data structures for in-memory cache
        pass

    def load(self, reqeust: LoadRequest):
        # Maybe return in-memory data, maybe call DataBroker.load
        pass

    def store(self, request: StoreRequest):
        # Maybe update in-memory data, call DataBroker.store
        pass

    @pyqtSignal(LoadResponse)
    def handle_loaded(self, response: LoadResponse):
        # Update in-memory data, emit loaded
        # Connected to TDataBroker.loaded
        pass

    @pyqtSignal(Failure)
    def handle_failed(self, failure: Failure):
        # Invalidate in-memory data, emit failed
        # Connected to TDataBroker.failed
        pass

class TSomeWidget:

    @pyqtSlot(LoadResponse)
    def handle_loaded(self, response: LoadResponse):
        # Create or update views and widgets with data from response
        # Connected to TDataCache.loaded
        pass

    @pyqtSlot(Failure)
    def handle_failed(self, failure: Failure):
        # Tell the user that something went wrong, maybe recover
        # Connected to TDataCache.failed
        pass
