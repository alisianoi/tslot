import pytest

from pendulum import DateTime
from src.ai.model import TSlotModel, TTaskModel, TTagModel, TEntryModel


def test_tag_model_0():

    tag = TTagModel(name='tag')

    assert tag.id is None
    assert tag.name == 'tag'

def test_tag_model_1():

    tag = TTagModel(name='tag', id=42)

    assert tag.id == 42
    assert tag.name == 'tag'

def test_tag_model_2():

    tag0 = TTagModel(name='tag')
    tag1 = TTagModel(name='tag')

    assert tag0 == tag1

def test_tag_model_3():

    tag0 = TTagModel(name='tag', id=42)
    tag1 = TTagModel(name='tag', id=42)

    assert tag0 == tag1

def test_tag_model_4():

    tag0 = TTagModel(name='tag', id=42)
    tag1 = TTagModel(name='tag')

    assert tag0 != tag1

def test_tag_model_5():

    tag0 = TTagModel(name='tag0')
    tag1 = TTagModel(name='tag1')

    assert tag0 < tag1

def test_tag_model_6():

    tag0 = TTagModel(name='tag0', id=42)
    tag1 = TTagModel(name='tag1')

    assert tag0 < tag1

def test_tag_model_7():

    tag0 = TTagModel(name='tag0')
    tag1 = TTagModel(name='tag0')

    assert tag0 <= tag1

def test_tag_model_8():

    with pytest.raises(TypeError) as error:
        tag = TTagModel()

    assert "missing 1 required positional argument: 'name'" in str(error.value)

def test_task_model_0():

    task = TTaskModel()

    assert task.id is None
    assert task.name is None

def test_task_model_1():

    task = TTaskModel(name='task')

    assert task.id is None
    assert task.name == 'task'

def test_task_model_2():

    task = TTaskModel(name='task', id=42)

    assert task.id == 42
    assert task.name == 'task'

def test_task_model_3():

    task0 = TTaskModel(name='task')
    task1 = TTaskModel(name='task')

    assert task0 == task1

def test_task_model_4():

    task0 = TTaskModel(name='task', id=42)
    task1 = TTaskModel(name='task', id=42)

    assert task0 == task1

def test_task_model_5():

    task0 = TTaskModel(name='task', id=42)
    task1 = TTaskModel(name='task')

    assert task0 != task1

def test_task_model_6():

    task0 = TTaskModel(name='task0')
    task1 = TTaskModel(name='task1')

    assert task0 < task1

def test_task_model_7():

    task0 = TTaskModel(name='task0', id=42)
    task1 = TTaskModel(name='task1')

    assert task0 < task1

def test_task_model_8():

    task0 = TTaskModel(name='task0')
    task1 = TTaskModel(name='task0')

    assert task0 <= task1

def test_slot_model_0():

    fst = DateTime.now()

    slot = TSlotModel(fst=fst)

    assert slot.id is None
    assert slot.fst == fst

def test_slot_model_1():

    fst = DateTime.now()

    slot = TSlotModel(fst=fst, id=42)

    assert slot.id == 42
    assert slot.fst == fst

def test_slot_model_2():

    fst = DateTime.now()

    slot0 = TSlotModel(fst=fst)
    slot1 = TSlotModel(fst=fst)

    assert slot0 == slot1

def test_slot_model_3():

    fst = DateTime.now()

    slot0 = TSlotModel(fst=fst, id=42)
    slot1 = TSlotModel(fst=fst, id=42)

    assert slot0 == slot1

def test_slot_model_4():

    fst = DateTime.now()

    slot0 = TSlotModel(fst=fst, id=42)
    slot1 = TSlotModel(fst=fst)

    assert slot0 != slot1

def test_slot_model_5():

    fst = DateTime.now()
    lst = DateTime.now()

    slot0 = TSlotModel(fst=fst, lst=lst)
    slot1 = TSlotModel(fst=fst, lst=lst)

    assert slot0 == slot1

def test_slot_model_6():

    fst = DateTime.now()
    lst = DateTime.now()

    slot0 = TSlotModel(fst=fst, lst=lst)
    slot1 = TSlotModel(fst=fst)

    assert slot0 != slot1

def test_slot_model_7():

    fst = DateTime.now()
    lst = DateTime.now()

    slot0 = TSlotModel(fst=fst)
    slot1 = TSlotModel(fst=lst)

    assert slot0 != slot1

def test_slot_model_8():

    with pytest.raises(TypeError) as error:
        tag = TSlotModel()

    assert "missing 1 required positional argument: 'fst'" in str(error.value)

def test_entry_model_0():

    fst = DateTime.now()

    slot = TSlotModel(fst=fst)
    entry = TEntryModel(slot=slot)

    assert entry.slot == slot
    assert entry.task == TTaskModel()
    assert entry.tags == []

def test_entry_model_1():

    fst = DateTime.now()
    lst = DateTime.now()

    slot = TSlotModel(fst=fst, lst=lst)
    task = TTaskModel(name='task')
    tags = [TTagModel(name='tag')]

    entry = TEntryModel(slot, task, tags)

    assert entry.slot == slot
    assert entry.task == task
    assert entry.tags == tags
