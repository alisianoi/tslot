import logging
import pprint
from pathlib import Path
from typing import List

from PyQt5.QtCore import QObject

from src.db.model import TagModel, TaskModel
from src.db.worker import TReader
from src.common.dto.tag_fetch_request import TTagsByNameFetchRequest
from src.common.dto.tag_fetch_response import TTagFetchResponse, TTagsByNameFetchResponse
from src.common.logger import logged


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

    @logged(logger=logging.getLogger('tslot-data'), disabled=True)
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


class TTagsByNameReader(TReader):

    def __init__(
        self
        , request: TTagsByNameFetchRequest
        , path   : Path=None
    ) -> None:

        super().__init__(request=request, path=path)

    @logged(logger=logging.getLogger('tslot-data'), disabled=True)
    def work(self):

        if self.session is None:
            self.session = self.create_session()

        if self.request.exact:
            TagByNameQuery = self.session.query(
                TagModel
            ).filter(
                TagModel.name == f'{self.request.name}'
            )
        else:
            TagByNameQuery = self.session.query(
                TagModel
            ).filter(
                TagModel.name.ilike(f'%{self.request.name}%')
            )

        tags = TagByNameQuery.all()

        # There could be zero, one or more tags in the response
        self.fetched.emit(TTagsByNameFetchResponse(tags=tags))

        self.session.close()

        self.stopped.emit()
