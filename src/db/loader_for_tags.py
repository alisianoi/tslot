import pprint

from pathlib import Path

from PyQt5.QtCore import QObject

from src.db.model import TagModel, TaskModel
from src.db.loader import TLoader, LoadFailed


class TTagLoader(TLoader):

    def __init__(
        self
        , tasks : list
        , path  : Path=None
        , parent: QObject=None
    ):

        super().__init__(path, parent)

        self.tasks = tasks

    def work(self):

        if not isinstance(self.tasks, list):
            return self.failed.emit(
                LoadFailed('Expected tasks to be a list')
            )

        if len(self.tasks) == 0:
            return self.loaded.emit([])

        task_ids = None

        if all(isinstance(task, int) for task in self.tasks):
            task_ids = self.tasks

        if all(isinstance(task, TaskModel) for task in self.tasks):
            task_ids = [task.id for task in self.tasks]

        if task_ids is None:
            return self.failed.emit(
                LoadFailed('Expected tasks to be a homogenous list')
            )

        result = self.session.query(
            TaskModel, TagModel
        ).filter(
            TaskModel.id.in_(task_ids), TagModel.tasks
        ).all()

        self.logger.debug(result)

        self.loaded.emit(result)

        self.session.close()

        self.stopped.emit()
