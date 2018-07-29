import pprint

from src.db.model import TagModel, TaskModel
from src.db.reader_for_tags import TTagReader


def setup_one_tag_one_task(session):

    tag_model = TagModel(name='tag0')
    task_model = TaskModel(name='task0')

    tag_model.tasks = [task_model]
    task_model.tags = [tag_model]

    session.add_all([tag_model, task_model])
    session.commit()

    return [tag_model], [task_model]

def setup_two_tags_one_task(session):

    tag_model0 = TagModel(name='tag0')
    tag_model1 = TagModel(name='tag1')

    task_model0 = TaskModel(name='task0')

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
