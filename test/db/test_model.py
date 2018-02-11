import pytest

import pprint

from datetime import datetime, timedelta

from src.db.model import TagModel, TaskModel, DateModel, SlotModel


def test_tag_model_0():

    tag = TagModel()

    assert tag.id is None
    assert tag.name is None
    assert isinstance(tag.tasks, list) and not tag.tasks

def test_tag_model_1():

    tag = TagModel(name='Tag0')

    assert tag.id is None
    assert tag.name == 'Tag0'

def test_tag_model_2():

    tag = TagModel(id=42, name='Tag0')

    assert tag.id == 42
    assert tag.name == 'Tag0'

def test_tag_model_eq_0():

    tag = TagModel()

    assert tag == tag

def test_tag_model_eq_1():
    tag0, tag1 = TagModel(), TagModel()

    assert tag0 == tag1

def test_tag_model_eq_2():

    tag0, tag1 = TagModel(name='tag'), TagModel(name='tag')

    assert tag0 == tag1

def test_tag_model_eq_3():

    tag0, tag1 = TagModel(name='tag0'), TagModel(name='tag1')

    assert tag0 != tag1
    assert not tag0 == tag1

def test_tag_model_hash_0():

    tag = TagModel()

    assert hash(tag) == hash(tag)

def test_tag_model_hash_1():

    tag0, tag1 = TagModel(), TagModel()

    assert tag0 == tag1
    assert hash(tag0) == hash(tag1)

def test_tag_model_hash_2():

    tag0, tag1 = TagModel(name='tag'), TagModel(name='tag')

    assert tag0 == tag1
    assert hash(tag0) == hash(tag1)

def test_tag_model_hash_3():

    tag0, tag1 = TagModel(name='tag0'), TagModel(name='tag1')

    assert tag0 != tag1
    assert hash(tag0) != hash(tag1)

def test_task_model_0():

    task = TaskModel()

    assert task.id is None
    assert task.name is None
    assert isinstance(task.tags, list) and not task.tags
    assert isinstance(task.slots, list) and not task.slots

def test_task_model_1():

    task = TaskModel(name='Task')

    assert task.id is None
    assert task.name == 'Task'
    assert isinstance(task.tags, list) and not task.tags
    assert isinstance(task.slots, list) and not task.slots

def test_task_model_eq_0():

    task = TaskModel()

    assert task == task

def test_task_model_eq_1():

    task0, task1 = TaskModel(), TaskModel()

    assert task0 == task1

def test_task_model_eq_2():

    task0, task1 = TaskModel(name='Task'), TaskModel(name='Task')

    assert task0 == task1

def test_task_model_eq_3():

    task0, task1 = TaskModel(name='Task0'), TaskModel(name='Task1')

    assert task0 != task1
    assert not task0 == task1

def test_task_model_hash_0():

    task = TaskModel()

    assert hash(task) == hash(task)

def test_task_model_hash_1():

    task0, task1 = TaskModel(), TaskModel()

    assert task0 == task1
    assert hash(task0) == hash(task1)

def test_task_model_hash_2():

    task0, task1 = TaskModel(name='Task'), TaskModel(name='Task')

    assert task0 == task1
    assert hash(task0) == hash(task1)

def test_task_model_hash_3():

    task0, task1 = TaskModel(name='Task0'), TaskModel(name='Task1')

    assert task0 != task1
    assert hash(task0) != hash(task1)

def test_date_model_0():

    dm = DateModel()

    assert dm.id is None
    assert dm.date is None
    assert isinstance(dm.slots, list) and not dm.slots

def test_date_model_1():

    d = datetime.utcnow().date()

    dm = DateModel(date=d)

    assert dm.id is None
    assert dm.date == d
    assert isinstance(dm.slots, list) and not dm.slots

def test_date_model_eq_0():

    dm = DateModel()

    assert dm == dm

def test_date_model_eq_1():

    dm0, dm1 = DateModel(), DateModel()

    assert dm0 == dm1

def test_date_model_eq_2():

    d = datetime.utcnow().date()

    dm0, dm1 = DateModel(date=d), DateModel(date=d)

    assert dm0 == dm1

def test_date_model_eq_3():

    d0 = datetime.utcnow().date()
    d1 = d0 - timedelta(days=42)

    dm0, dm1 = DateModel(date=d0), DateModel(date=d1)

    assert dm0 != dm1
    assert not dm0 == dm1

def test_date_model_lt_0():

    dm = DateModel()

    with pytest.raises(TypeError) as e:
        dm < dm

def test_date_model_lt_1():

    dm = DateModel(date=datetime.utcnow().date())

    assert not dm < dm

def test_date_model_lt_2():

    dm0, dm1 = DateModel(), DateModel()

    with pytest.raises(TypeError) as e:
        dm0 < dm1

    with pytest.raises(TypeError) as e:
        dm1 < dm0

def test_date_model_lt_3():

    dm0, dm1 = DateModel(date=datetime.utcnow().date()), DateModel()

    with pytest.raises(TypeError) as e:
        dm0 < dm1

    with pytest.raises(TypeError) as e:
        dm1 < dm0

def test_date_model_lt_4():

    d0 = datetime.utcnow().date()
    d1 = d0 - timedelta(days=42)

    dm0, dm1 = DateModel(date=d0), DateModel(date=d1)

    assert not dm0 < dm1
    assert     dm1 < dm0

def test_date_model_lt_5():

    d = datetime.utcnow().date()

    dm0, dm1 = DateModel(date=d), DateModel(date=d)

    assert not dm0 < dm1

def test_date_model_le_0():

    dm = DateModel()

    with pytest.raises(TypeError) as e:
        dm <= dm

def test_date_model_le_1():

    dm = DateModel(date=datetime.utcnow().date())

    assert dm <= dm

def test_date_model_le_2():

    dm0, dm1 = DateModel(), DateModel()

    with pytest.raises(TypeError) as e:
        dm0 <= dm1

    with pytest.raises(TypeError) as e:
        dm1 <= dm0

def test_date_model_le_3():

    dm0, dm1 = DateModel(date=datetime.utcnow().date()), DateModel()

    with pytest.raises(TypeError) as e:
        dm0 <= dm1

    with pytest.raises(TypeError) as e:
        dm1 <= dm0

def test_date_model_le_4():

    d0 = datetime.utcnow().date()
    d1 = d0 - timedelta(days=42)

    dm0, dm1 = DateModel(date=d0), DateModel(date=d1)

    assert not dm0 <= dm1
    assert     dm1 <= dm0

def test_date_model_le_5():

    d = datetime.utcnow().date()

    dm0, dm1 = DateModel(date=d), DateModel(date=d)

    assert dm0 <= dm1

def test_date_model_gt_0():

    dm = DateModel()

    with pytest.raises(TypeError) as e:
        dm > dm

def test_date_model_gt_1():

    dm = DateModel(date=datetime.utcnow().date())

    assert not dm > dm

def test_date_model_gt_2():

    dm0, dm1 = DateModel(), DateModel()

    with pytest.raises(TypeError) as e:
        dm0 > dm1

    with pytest.raises(TypeError) as e:
        dm1 > dm0

def test_date_model_gt_3():

    dm0, dm1 = DateModel(date=datetime.utcnow().date()), DateModel()

    with pytest.raises(TypeError) as e:
        dm0 > dm1

    with pytest.raises(TypeError) as e:
        dm1 > dm0

def test_date_model_gt_4():

    d0 = datetime.utcnow().date()
    d1 = d0 - timedelta(days=42)

    dm0, dm1 = DateModel(date=d0), DateModel(date=d1)

    assert     dm0 > dm1
    assert not dm1 > dm0

def test_date_model_gt_5():

    d = datetime.utcnow().date()

    dm0, dm1 = DateModel(date=d), DateModel(date=d)

    assert not dm0 > dm1

def test_date_model_ge_0():

    dm = DateModel()

    with pytest.raises(TypeError) as e:
        dm >= dm

def test_date_model_ge_1():

    dm = DateModel(date=datetime.utcnow().date())

    assert dm >= dm

def test_date_model_ge_2():

    dm0, dm1 = DateModel(), DateModel()

    with pytest.raises(TypeError) as e:
        dm0 >= dm1

    with pytest.raises(TypeError) as e:
        dm1 >= dm0

def test_date_model_ge_3():

    dm0, dm1 = DateModel(date=datetime.utcnow().date()), DateModel()

    with pytest.raises(TypeError) as e:
        dm0 >= dm1

    with pytest.raises(TypeError) as e:
        dm1 >= dm0

def test_date_model_ge_4():

    d0 = datetime.utcnow().date()
    d1 = d0 - timedelta(days=42)

    dm0, dm1 = DateModel(date=d0), DateModel(date=d1)

    assert     dm0 >= dm1
    assert not dm1 >= dm0

def test_date_model_ge_5():

    d = datetime.utcnow().date()

    dm0, dm1 = DateModel(date=d), DateModel(date=d)

    assert dm0 >= dm1

def test_date_model_hash_0():

    dm = DateModel()

    assert hash(dm) == hash(dm)

def test_date_model_hash_1():

    dm = DateModel(date=datetime.utcnow().date())

    assert dm == dm
    assert hash(dm) == hash(dm)

def test_date_model_hash_2():

    dm0, dm1 = DateModel(), DateModel()

    assert dm0 == dm1
    assert hash(dm0) == hash(dm1)

def test_date_model_hash_3():

    d = datetime.utcnow().date()

    dm0, dm1 = DateModel(date=d), DateModel(date=d)

    assert dm0 == dm1
    assert hash(dm0) == hash(dm1)

def test_date_model_hash_4():

    d0 = datetime.utcnow().date()
    d1 = d0 - timedelta(days=42)

    dm0, dm1 = DateModel(date=d0), DateModel(date=d1)

    assert dm0 != dm1
    assert hash(dm0) != hash(dm1)

def test_slot_model_0():

    slot = SlotModel()

    assert slot.id is None
    assert slot.fst is None
    assert slot.lst is None
    assert slot.task_id is None
    assert slot.date_id is None
    assert slot.task is None
    assert slot.date is None

def test_slot_model_1():

    fst = datetime.utcnow().date()
    lst = datetime.utcnow().date() + timedelta(microseconds=1)

    slot = SlotModel(fst=fst, lst=lst)

    assert slot.id is None
    assert slot.fst == fst
    assert slot.lst == lst
    assert slot.task_id is None
    assert slot.date_id is None
    assert slot.task is None
    assert slot.date is None

def test_slot_model_eq_0():

    slot = SlotModel()

    assert slot == slot

def test_slot_model_eq_1():

    fst = datetime.utcnow().date()
    lst = datetime.utcnow().date() + timedelta(microseconds=1)

    slot = SlotModel(fst=fst, lst=lst)

    assert slot == slot

def test_slot_model_eq_2():

    fst = datetime.utcnow().date()
    lst = datetime.utcnow().date() + timedelta(microseconds=1)

    slot0 = SlotModel(fst=fst, lst=lst)
    slot1 = SlotModel(fst=fst, lst=lst)

    assert slot0 == slot1

def test_slot_model_eq_3():

    fst0 = datetime.utcnow().date()
    lst0 = datetime.utcnow().date() + timedelta(microseconds=1)

    fst1 = fst0 - timedelta(days=1)
    lst1 = lst0 - timedelta(days=1)

    slot0 = SlotModel(fst=fst0, lst=lst0)
    slot1 = SlotModel(fst=fst1, lst=lst1)

    assert slot0 != slot1
    assert not slot0 == slot1

def test_slot_model_lt_0():

    slot = SlotModel()

    with pytest.raises(TypeError) as e:
        slot < slot

def test_slot_model_lt_1():

    slot0, slot1 = SlotModel(), SlotModel()

    with pytest.raises(TypeError) as e:
        slot0 < slot1

    with pytest.raises(TypeError) as e:
        slot1 < slot0

def test_slot_model_lt_2():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0, slot1 = SlotModel(fst=fst, lst=lst), SlotModel

    with pytest.raises(TypeError) as e:
        slot0 < slot1

    with pytest.raises(TypeError) as e:
        slot1 < slot0

def test_slot_model_lt_3():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0 = SlotModel(fst=fst, lst=lst)
    slot1 = SlotModel(fst=fst, lst=lst)

    assert not slot0 < slot1
    assert not slot1 < slot0

def test_slot_model_lt_4():

    fst0 = datetime.utcnow().date()
    lst0 = fst0 + timedelta(microseconds=1)

    fst1 = fst0 - timedelta(days=1)
    lst1 = lst0 - timedelta(days=1)

    slot0 = SlotModel(fst=fst0, lst=lst0)
    slot1 = SlotModel(fst=fst1, lst=lst1)

    assert not slot0 < slot1
    assert     slot1 < slot0

def test_slot_model_le_0():

    slot = SlotModel()

    with pytest.raises(TypeError) as e:
        slot <= slot

def test_slot_model_le_1():

    slot0, slot1 = SlotModel(), SlotModel()

    with pytest.raises(TypeError) as e:
        slot0 <= slot1

    with pytest.raises(TypeError) as e:
        slot1 <= slot0

def test_slot_model_le_2():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0, slot1 = SlotModel(fst=fst, lst=lst), SlotModel

    with pytest.raises(TypeError) as e:
        slot0 <= slot1

    with pytest.raises(TypeError) as e:
        slot1 <= slot0

def test_slot_model_le_3():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0 = SlotModel(fst=fst, lst=lst)
    slot1 = SlotModel(fst=fst, lst=lst)

    assert slot0 <= slot1
    assert slot1 <= slot0

def test_slot_model_le_4():

    fst0 = datetime.utcnow().date()
    lst0 = fst0 + timedelta(microseconds=1)

    fst1 = fst0 - timedelta(days=1)
    lst1 = lst0 - timedelta(days=1)

    slot0 = SlotModel(fst=fst0, lst=lst0)
    slot1 = SlotModel(fst=fst1, lst=lst1)

    assert not slot0 <= slot1
    assert     slot1 <= slot0

def test_slot_model_gt_0():

    slot = SlotModel()

    with pytest.raises(TypeError) as e:
        slot > slot

def test_slot_model_gt_1():

    slot0, slot1 = SlotModel(), SlotModel()

    with pytest.raises(TypeError) as e:
        slot0 > slot1

    with pytest.raises(TypeError) as e:
        slot1 > slot0

def test_slot_model_gt_2():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0, slot1 = SlotModel(fst=fst, lst=lst), SlotModel

    with pytest.raises(TypeError) as e:
        slot0 > slot1

    with pytest.raises(TypeError) as e:
        slot1 > slot0

def test_slot_model_gt_3():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0 = SlotModel(fst=fst, lst=lst)
    slot1 = SlotModel(fst=fst, lst=lst)

    assert not slot0 > slot1
    assert not slot1 > slot0

def test_slot_model_gt_4():

    fst0 = datetime.utcnow().date()
    lst0 = fst0 + timedelta(microseconds=1)

    fst1 = fst0 - timedelta(days=1)
    lst1 = lst0 - timedelta(days=1)

    slot0 = SlotModel(fst=fst0, lst=lst0)
    slot1 = SlotModel(fst=fst1, lst=lst1)

    assert     slot0 > slot1
    assert not slot1 > slot0

def test_slot_model_ge_0():

    slot = SlotModel()

    with pytest.raises(TypeError) as e:
        slot >= slot

def test_slot_model_ge_1():

    slot0, slot1 = SlotModel(), SlotModel()

    with pytest.raises(TypeError) as e:
        slot0 >= slot1

    with pytest.raises(TypeError) as e:
        slot1 >= slot0

def test_slot_model_ge_2():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0, slot1 = SlotModel(fst=fst, lst=lst), SlotModel

    with pytest.raises(TypeError) as e:
        slot0 >= slot1

    with pytest.raises(TypeError) as e:
        slot1 >= slot0

def test_slot_model_ge_3():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0 = SlotModel(fst=fst, lst=lst)
    slot1 = SlotModel(fst=fst, lst=lst)

    assert slot0 >= slot1
    assert slot1 >= slot0

def test_slot_model_ge_4():

    fst0 = datetime.utcnow().date()
    lst0 = fst0 + timedelta(microseconds=1)

    fst1 = fst0 - timedelta(days=1)
    lst1 = lst0 - timedelta(days=1)

    slot0 = SlotModel(fst=fst0, lst=lst0)
    slot1 = SlotModel(fst=fst1, lst=lst1)

    assert     slot0 >= slot1
    assert not slot1 >= slot0

def test_slot_model_hash_0():

    slot = SlotModel()

    assert slot == slot
    assert hash(slot) == hash(slot)

def test_slot_model_hash_1():

    fst = datetime.utcnow().date()

    slot = SlotModel(fst=fst)

    assert slot == slot
    assert hash(slot) == hash(slot)

def test_slot_model_hash_2():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot = SlotModel(fst=fst, lst=lst)

    assert slot == slot
    assert hash(slot) == hash(slot)

def test_slot_model_hash_3():

    slot0, slot1 = SlotModel(), SlotModel()

    assert slot0 == slot1
    assert hash(slot0) == hash(slot1)

def test_slot_model_hash_4():

    fst = datetime.utcnow().date()

    slot0, slot1 = SlotModel(fst=fst), SlotModel()

    assert slot0 != slot1
    assert not slot0 == slot1
    assert hash(slot0) != hash(slot1)

def test_slot_model_hash_5():

    fst = datetime.utcnow().date()

    slot0, slot1 = SlotModel(fst=fst), SlotModel(fst=fst)

    assert slot0 == slot1
    assert hash(slot0) == hash(slot1)

def test_slot_model_hash_6():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0, slot1 = SlotModel(fst=fst, lst=lst), SlotModel(fst=fst)

    assert slot0 != slot1
    assert not slot0 == slot1
    assert hash(slot0) != hash(slot1)

def test_slot_model_hash_7():

    fst = datetime.utcnow().date()
    lst = fst + timedelta(microseconds=1)

    slot0 = SlotModel(fst=fst, lst=lst)
    slot1 = SlotModel(fst=fst, lst=lst)

    assert slot0 == slot1
    assert hash(slot0) == hash(slot1)
