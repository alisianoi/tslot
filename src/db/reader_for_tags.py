import pprint

from pathlib import Path

from PyQt5.QtCore import QObject

from src.db.model import TagModel, TaskModel
from src.db.worker import TReader

from src.msg.fetch_tag import TTagFetchResponse

class TTagReader(TReader):
    """Fetch a list of tags when supplied with a list of tasks"""

    def __init__(
        self
        , tasks : list
        , path  : Path=None
        , parent: QObject=None
    ) -> None:

        super().__init__(path, parent)

        self.tasks = tasks

    def work(self):

        if not isinstance(self.tasks, list):
            return self.failed.emit(LoadFailure('Expected tasks to be a list'))

        if len(self.tasks) == 0:
            return self.loaded.emit([])

        task_ids = None

        if all(isinstance(task, int) for task in self.tasks):
            task_ids = self.tasks

        if all(isinstance(task, TaskModel) for task in self.tasks):
            task_ids = [task.id for task in self.tasks]

        if task_ids is None:
            return self.failed.emit(LoadFailure('Failed to construct task_ids'))

        result = self.session.query(
            TaskModel, TagModel
        ).filter(
            TaskModel.id.in_(task_ids), TagModel.tasks
        ).all()

        self.logger.debug(result)

        self.fetched.emit(TTagFetchResponse(tags=result))

        self.session.close()

        self.stopped.emit()
