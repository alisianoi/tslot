from pathlib import Path
from typing import List

from PyQt5.QtCore import QObject

from src.common.dto.model import TEntryModel, TSlotModel, TTagModel, TTaskModel
from src.common.request.stash.entry_stash_request import TEntryStashRequest
from src.common.response.stash.entry_stash_response import TEntryStashResponse
from src.db.model import Base, SlotModel, TagModel, TaskModel
from src.db.worker import TWriter


class TEntryWriter(TWriter):

    def __init__(
        self
        , request: TEntryStashRequest
        , path   : Path = None
        , parent : QObject = None
    ):

        super().__init__(request, path, parent)

        self.items = request.items

    def work(self):

        if len(self.items) != 1:
            raise RuntimeError('Expecting to have to save exactly one entry')

        item = self.items[0]

        if self.session is None:
            self.session = self.create_session()

        slot = self.choose_old_or_new_slot(item.slot)
        task = self.choose_old_or_new_task(item.task)

        # Either the id should be None (i.e. the model is new) or both should be
        # not None (i.e. the model is old). Must be always equal though:
        if slot.id != item.slot.id:
            raise RuntimeError(f'Could not find slot with id {item.slot.id}')
        if task.id != item.task.id:
            raise RuntimeError(f'Could not find task with id {item.task.id}')

        # Note: add another check that if you took an old slot/task and made it
        # overlap with a different old slot/task, the check should fail too. For
        # the simple case (of task names) consider using DB constraints instead.
        if slot.id == None:
            self.check_slot_overlap(item.slot)
        if task.id == None:
            self.check_task_overlap(item.task)

        tags = self.choose_old_or_new_tags(item.tags)

        slot.task = task
        task.tags = tags

        if slot.id is None:
            self.session.add(slot)
        else:
            self.session.query(
                SlotModel
            ).filter(
                SlotModel.id == slot.id
            ).update(
                {'name': slot.name, 'task': slot.task}
            )

        if task.id is None:
            self.session.add(task)
        else:
            self.session.query(
                TaskModel
            ).filter(
                TaskModel.id == task.id
            ).update(
                {'name': task.name, 'tags': task.tags}
            )

        for tag in tags:
            if tag.id is None:
                self.session.add(tag)
            else:
                self.session.query(
                    TagModel.id == tag.id
                ).update(
                    {'name': tag.name}
                )

        self.session.commit()

        self.stashed.emit(
            TEntryStashResponse([
                TEntryModel(
                    slot=TSlotModel.from_model(slot)
                    , task=TTaskModel.from_model(task)
                    , tags=[TTagModel.from_model(tag) for tag in tags]
                )
            ])
        )

        self.session.close()

    def choose_old_or_new_slot(self, item: TSlotModel) -> SlotModel:

        if item is None:
            raise RuntimeError('Cannot write an entry without a slot')

        slot = self.fetch_by_id_or_new(SlotModel, item.id)

        slot.fst, slot.lst = item.fst, item.lst

        return slot

    def choose_old_or_new_task(self, item: TTaskModel) -> TaskModel:

        if item is None:
            return TaskModel()

        task = self.fetch_by_id_or_new(TaskModel, item.id)

        task.name = item.name

        return task

    def fetch_by_id_or_new(self, model: Base, id: int) -> Base:

        if id is None:
            return model()

        return self.session.query(model).filter(model.id == id).first()

    def choose_old_or_new_tags(self, items: List[TTagModel]) -> List[TagModel]:
        """
        Given a list of tags, figure out which of them require what action

        There may be tags that:
        1. have an existing database id and old name, so need no update
        2. have an existing database id and new name, so need a name update
        3. have no database id and a fresh name, so need to be created
        4. have no database id and an existing name, so need to have that id
        """

        old_tags, new_tags = [], []

        for item in items:
            if item.id is None:
                new_tags.append(item)
            else:
                old_tags.append(item)

        old_tags = self.build_old_tags(old_tags)
        new_tags = self.build_new_tags(new_tags)

        return old_tags + new_tags

    def check_slot_overlap(self, item: TSlotModel):
        # TODO: this is potentially a *very* long check, implement it later.
        # Maybe check it with database constraints somehow, I dunno.

        pass

    def check_task_overlap(self, item: TTaskModel):

        task = self.session.query(
            TaskModel
        ).filter(
            TaskModel.name == item.name
        ).first()

        if task != None:
            raise RuntimeError('Task with this name already exists')

    def build_old_tags(self, xs: List[TTagModel]) -> List[TagModel]:
        """
        Since these are "old" tags, they all have an id that is not None. Make
        sure that all tags have a pre-existing pair in the database (by id).
        """

        ys = self.session.query(
            TagModel
        ).filter(
            TagModel.id.in_([tag.id for tag in xs])
        ).all()

        xs.sort(key=lambda tag: tag.id)
        ys.sort(key=lambda tag: tag.id)

        for i in range(1, len(xs)):
            if xs[i].id == xs[i - 1].id:
                raise RuntimeError('Tags from GUI have reoccuring ids')
        for i in range(1, len(ys)):
            if ys[i].id == ys[i - 1].id:
                raise RuntimeError('Tags from Database have reoccuring ids')

        i, j = 0, 0
        unpaired_xs, unpaired_ys = [], []

        while i != len(xs) and j != len(ys):
            if xs[i].id == ys[j].id:
                i += 1
                j += 1
            elif xs[i].id < ys[j].id:
                unpaired_xs.append(xs[i])

                i += 1
            elif xs[i].id > ys[j].id:
                unpaired_ys.append(ys[j])

                j += 1

        if i != len(xs):
            unpaired_xs.extend(xs[i:])
        if j != len(ys):
            unpaired_ys.extend(ys[j:])

        if unpaired_xs or unpaired_ys:
            raise RuntimeError(
                'Unpaired tags: {unpaired_xs}, {unpaired_ys}'
            )

        for x, y in zip(xs, ys):
            y.name = x.name

        return ys

    def build_new_tags(self, xs: List[TTagModel]) -> List[TagModel]:

        ys = self.session.query(
            TagModel
        ).filter(
            TagModel.name.in_([tag.name for tag in xs])
        ).all()

        xs.sort(key=lambda tag: tag.name)
        ys.sort(key=lambda tag: tag.name)

        for i in range(1, len(xs)):
            if xs[i].name == xs[i - 1].name:
                raise RuntimeError('Tags from GUI have reoccuring names')
        for i in range(1, len(ys)):
            if ys[i].name == ys[i - 1].name:
                raise RuntimeError('Tags from Database have reoccuring names')

        i, j = 0, 0
        tag_pairs = []

        while i != len(xs) and j != len(ys):
            if xs[i].name == ys[j].name:
                # The user typed in a "new" tag that has the same name as a tag
                # from the database. Assume the user wants the existing tag.
                tag_pairs.append((xs[i], ys[j]))

                i += 1
                j += 1
            elif xs[i].name < ys[j].name:
                tag_pairs.append((xs[i], TagModel()))

                i += 1
            elif xs[i].name > ys[j].name:
                raise RuntimeError(
                    'Expected tags from Database to be a subset of GUI tags'
                )

        tag_pairs.extend([(tag, TagModel()) for tag in xs[i:]])

        for x, y in tag_pairs:
            y.name = x.name

        return [tag for _, tag in tag_pairs]
