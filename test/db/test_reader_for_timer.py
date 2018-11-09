import pendulum

from src.db.reader_for_timer import TTimerReader
from src.msg.timer_fetch_request import TTimerFetchRequest

from test.db.test_reader import put_one_date


def test_single_timer_0(session, qtbot):
    """Fetch a timer from an empty database to get no results."""

    worker = TTimerReader(TTimerFetchRequest())

    worker.session = session

    def handle_fetched(response):

        assert response.timer is None

    def handle_alerted(response):

        assert False

    worker.fetched.connect(handle_fetched)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.fetched, timeout=1000) as blocker:
        blocker.connect(worker.alerted)

        worker.work()


def test_single_timer_1(session, qtbot):
    """Fetch a single timer from the database that only has that one timer."""

    fst = pendulum.datetime(year=2010, month=6, day=15, tz="UTC")
    fst.replace(hour=10, minute=30, second=0, microsecond=0)

    put_one_date(session, fst=fst, lst=None, name=None)

    worker = TTimerReader(TTimerFetchRequest())

    worker.session = session

    def handle_fetched(response):

        assert response.timer is not None
        assert response.timer.slot.fst == fst

    def handle_alerted(response):

        assert False

    worker.fetched.connect(handle_fetched)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.fetched, timeout=1000) as blocker:
        blocker.connect(worker.alerted)

        worker.work()
