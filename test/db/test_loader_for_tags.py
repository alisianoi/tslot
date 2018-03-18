import pprint

from src.db.model import TagModel, TaskModel
from src.db.loader_for_tags import TTagLoader


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

def test_tag_loader_0(session, qtbot):
    
    tags, tasks = setup_one_tag_one_task(session)

    worker = TTagLoader(tasks=tasks)

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == 1

        for entry in entries:
            task, tag = entry

            assert tag in task.tags
            assert task in tag.tasks

    def handle_failed(reason):
        assert False, reason

    worker.loaded.connect(handle_loaded)
    worker.failed.connect(handle_failed)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        blocker.connect(worker.failed)

        worker.work()

def test_tag_loader_1(session, qtbot):

    tags, tasks = setup_two_tags_one_task(session)

    worker = TTagLoader(tasks=tasks)

    worker.session = session

    def handle_loaded(entries):
        assert len(entries) == 2

        for entry in entries:

            task, tag = entry

            assert tag in task.tags
            assert task in tag.tasks

    def handle_failed(reason):
        assert False, reason

    worker.loaded.connect(handle_loaded)
    worker.failed.connect(handle_failed)

    with qtbot.waitSignal(worker.loaded, timeout=1000) as blocker:
        blocker.connect(worker.failed)

        worker.work()
