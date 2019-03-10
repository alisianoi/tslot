import pprint

import pytest

from src.common.request.fetch.tag_fetch_request import TTagsByNameFetchRequest
from src.common.response.fetch.tag_fetch_response import \
    TTagsByNameFetchResponse
from src.db.model import TagModel, TaskModel
from src.db.reader_for_tags import TTagReader, TTagsByNameReader


def setup_one_tag_one_task(session):

    tag_model = TagModel(name="tag0")
    task_model = TaskModel(name="task0")

    tag_model.tasks = [task_model]
    task_model.tags = [tag_model]

    session.add_all([tag_model, task_model])
    session.commit()

    return [tag_model], [task_model]


def setup_two_tags_one_task(session):

    tag_model0 = TagModel(name="tag0")
    tag_model1 = TagModel(name="tag1")

    task_model0 = TaskModel(name="task0")

    task_model0.tags = [tag_model0, tag_model1]

    session.add(task_model0)
    session.commit()

    return [tag_model0, tag_model1], [task_model0]


def test_tag_reader_0(session, qtbot):

    tags, tasks = setup_one_tag_one_task(session)

    worker = TTagReader(tasks=tasks)

    worker.session = session

    def handle_fetched(response):
        entries = response.tags

        assert len(entries) == 1

        for entry in entries:
            task, tag = entry

            assert tag in task.tags
            assert task in tag.tasks

    def handle_alerted(reason):
        assert False, reason

    worker.fetched.connect(handle_fetched)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.fetched, timeout=1000) as blocker:
        blocker.connect(worker.alerted)

        worker.work()


def test_tag_reader_1(session, qtbot):

    tags, tasks = setup_two_tags_one_task(session)

    worker = TTagReader(tasks=tasks)

    worker.session = session

    def handle_fetched(response):
        entries = response.tags

        assert len(entries) == 2

        for entry in entries:

            task, tag = entry

            assert tag in task.tags
            assert task in tag.tasks

    def handle_alerted(reason):
        assert False, reason

    worker.fetched.connect(handle_fetched)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.fetched, timeout=1000) as blocker:
        blocker.connect(worker.alerted)

        worker.work()


@pytest.mark.parametrize("exact", [True, False])
def test_tag_reader_2(session, qtbot, exact):
    """
    Create a single tag and fetch it using its exact name.

    Use both exact=True and exact=False in the request, it should produce the
    same result since there is only one tag in the database.
    """

    tag, task = setup_one_tag_one_task(session)

    request = TTagsByNameFetchRequest(name="tag0", exact=exact)

    worker = TTagsByNameReader(request=request)

    worker.session = session

    def handle_fetched(response: TTagsByNameFetchResponse):

        tags = response.tags

        assert len(tags) == 1

        assert tags[0] == tag[0]

    def handle_alerted(reason):
        assert False, reason

    worker.fetched.connect(handle_fetched)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.fetched, timeout=1000) as blocker:
        blocker.connect(worker.alerted)

        worker.work()


def test_tag_reader_3(session, qtbot):
    """Create a single tag and fetch it using the wrong exact name"""

    tag, task = setup_one_tag_one_task(session)

    # The name of the created tag is "tag0", i.e. with zero at the end
    request = TTagsByNameFetchRequest(name="tag", exact=True)

    worker = TTagsByNameReader(request=request)

    worker.session = session

    def handle_fetched(response: TTagsByNameFetchResponse):

        tags = response.tags

        assert len(tags) == 0

    def handle_alerted(reason):
        assert False, reason

    worker.fetched.connect(handle_fetched)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.fetched, timeout=1000) as blocker:
        blocker.connect(worker.alerted)

        worker.work()


@pytest.mark.parametrize(
    "name", ["tag", "Tag", "TAG", "tAg", "tAG", "ag", "AG", "aG", "0", "tag0"]
)
def test_tag_reader_4(session, qtbot, name):
    """
    Create a single tag name and fetch it using an incomplete name.

    Use exact=False in the request, so that the tag is actually found.
    """

    tag, task = setup_one_tag_one_task(session)

    request = TTagsByNameFetchRequest(name=name, exact=False)

    worker = TTagsByNameReader(request)
    worker.session = session

    def handle_fetched(response: TTagsByNameFetchResponse):

        assert len(response.tags) == 1
        assert response.tags == tag

    def handle_alerted(reason):
        assert False, reason

    worker.fetched.connect(handle_fetched)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.fetched, timeout=1000) as blocker:
        blocker.connect(worker.alerted)

        worker.work()


@pytest.mark.parametrize("name", ["hello", "ga", "gat", "at", "t0"])
def test_tag_reader_5(session, qtbot, name):
    """
    Create a single tag and fetch it using the wrong name.

    Even though exact=True is set on the request, the response should be empty.
    """

    tag, task = setup_one_tag_one_task(session)

    request = TTagsByNameFetchRequest(name=name, exact=False)

    worker = TTagsByNameReader(request)
    worker.session = session

    def handle_fetched(response: TTagsByNameFetchResponse):

        assert len(response.tags) == 0

    def handle_alerted(reason):
        assert False, reason

    worker.fetched.connect(handle_fetched)
    worker.alerted.connect(handle_alerted)

    with qtbot.waitSignal(worker.fetched, timeout=1000) as blocker:
        blocker.connect(worker.alerted)

        worker.work()
