import pendulum
import pytest

from pathlib import Path

from src.db.model import Base, SlotModel, TaskModel


def put_one_date(session, fst, lst, name=None):
    """
    Put one task at the given time slot into the provided database session
    """

    if name is None:
        name = 'task'

    slot_model = SlotModel(fst=fst, lst=lst)
    task_model = TaskModel(name=name)

    task_model.slots = [slot_model]
    slot_model.task = task_model

    session.add_all([slot_model, task_model])
    session.commit()


def setup_one_slot_whole_date(session, dt=None):
    """
    Put one slot into the database that will occupy the entire date
    """

    if dt is None:
        dt = pendulum.datetime(year=2010, month=6, day=15, tz='utc')

    fst, lst = dt.start_of('day'), dt.end_of('day')

    put_one_date(session, fst, lst)

    return [(fst, lst)]


def setup_one_slot_one_date(session, dt=None):
    """
    Put one one-hour slot into the database
    """

    if dt is None:
        dt = pendulum.datetime(year=2010, month=6, day=15, tz='utc')

    fst = dt.replace(hour=11, minute=30, second=0, microsecond=0)
    lst = dt.replace(hour=12, minute=30, second=0, microsecond=0)

    put_one_date(session, fst, lst)

    return [(fst, lst)]


def setup_two_slots_one_date(session, dt=None):
    """
    Put two one-hour same-date slots into the database

    Return those slots ordered past_to_future for date and for time
    """

    if dt is None:
        dt = pendulum.datetime(year=2010, month=6, day=15, tz='utc')

    fst0 = dt.replace(hour=5, minute=0, second=0, microsecond=0)
    lst0 = dt.replace(hour=6, minute=0, second=0, microsecond=0)

    fst1 = dt.replace(hour=19, minute=0, second=0, microsecond=0)
    lst1 = dt.replace(hour=20, minute=0, second=0, microsecond=0)

    put_one_date(session, fst0, lst0)
    put_one_date(session, fst1, lst1)

    return [(fst0, lst0), (fst1, lst1)]


def setup_two_slots_two_dates(session, dt=None):
    """
    Put two dates with one one-hour slot each into the database

    Return those slots ordered past_to_future for date and for time
    """

    if dt is None:
        dt = pendulum.datetime(year=2010, month=6, day=15, tz='utc')

    slots = []

    for day in [10, 20]:
        slots.extend(setup_one_slot_one_date(session, dt.replace(day=day)))

    return slots


def setup_four_slots_two_dates(session, dt=None):
    """
    Put two dates with two one-hour slots each into the database

    Return those slots ordered past_to_future for date and for time
    """

    if dt is None:
        dt = pendulum.datetime(year=2010, month=6, day=15, tz='utc')

    slots = []

    for day in [10, 20]:
        slots.extend(
            setup_two_slots_one_date(session, dt.replace(day=day))
        )

    return slots
