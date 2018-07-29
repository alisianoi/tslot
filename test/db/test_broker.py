import pytest

import pprint
import sqlite3

from pathlib import Path
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from PyQt5.QtCore import *

from src.db.broker import TDiskBroker
from src.db.model import TagModel, TaskModel, SlotModel

def utc_to_local(utc_dt):
    '''
    Convert UTC+00:00 time to UTC+XX:YY local time
    '''

    return utc_dt.replace(tzinfo=timezone.utc).astimezone(tzinfo=None)
