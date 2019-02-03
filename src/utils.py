import datetime
import logging.config
from functools import wraps
from typing import List

from PyQt5.QtCore import *
from PyQt5.QtWidgets import QStyleOption

import pendulum


def item_flags_as_str(flags: Qt.ItemFlags) -> str:

    message = ''

    if flags == 0:
        message = 'NoItemFlags'
    if flags & Qt.ItemIsSelectable:
        message += 'ItemIsSelectable '
    if flags & Qt.ItemIsEditable:
        message += 'ItemIsEditable '
    if flags & Qt.ItemIsDragEnabled:
        message += 'ItemIsDragEnabled '
    if flags & Qt.ItemIsDropEnabled:
        message += 'ItemIsDropEnabled '
    if flags & Qt.ItemIsUserCheckable:
        message += 'ItemIsUserCheckable '
    if flags & Qt.ItemIsEnabled:
        message += 'ItemIsEnabled '
    if flags & Qt.ItemIsAutoTristate:
        message += 'ItemIsAutoTristate '
    if flags & Qt.ItemIsTristate:
        message += 'ItemIsTristate '
    if flags & Qt.ItemNeverHasChildren:
        message += 'ItemNeverHasChildren '
    if flags & Qt.ItemIsUserTristate:
        message += 'ItemIsUserTristate '

    return message.strip()

def style_option_as_str(option: QStyleOption) -> str:

    if option == 1:
        return 'SO_FocusRect'
    elif option == 2:
        return 'SO_Button'
    elif option == 10:
        return 'SO_ViewItem'

    raise RuntimeError(f'Unknown style option type {type}')

def orient2str(orientation: Qt.Orientation):
    if orientation == 0x1 and orientation == Qt.Horizontal:
        return 'Qt.Hhttp://doc.qt.io/qt-5/qsize.html#detailsorizontal'
    elif orientation == 0x2 and orientation == Qt.Vertical:
        return 'Qt.Vertical'

    return f'Unknown Orientation (wrong number?): {orientation}'

def role2str(role: Qt.ItemDataRole):
    if role == 0 and role == Qt.DisplayRole:
        return 'Qt.DisplayRole'
    elif role == 1 and role == Qt.DecorationRole:
        return 'Qt.DecorationRole'
    elif role == 2 and role == Qt.EditRole:
        return 'Qt.EditRole'
    elif role == 3 and role == Qt.ToolTipRole:
        return 'Qt.ToolTipRole'
    elif role == 4 and role == Qt.StatusTipRole:
        return 'Qt.StatusTipRole'
    elif role == 5 and role == Qt.WhatsThisRole:
        return 'Qt.WhatsThisRole'
    elif role == 6 and role == Qt.FontRole:
        return 'Qt.FontRole'
    elif role == 7 and role == Qt.TextAlignmentRole:
        return 'Qt.TextAlignmentRole'
    elif role == 8 and role == Qt.BackgroundRole:
        return 'Qt.BackgroundRole'
    elif role == 9 and role == Qt.ForegroundRole:
        return 'Qt.ForegroundRole'
    elif role == 10 and role == Qt.CheckStateRole:
        return 'Qt.CheckStateRole'
    elif role == 11 and role == Qt.AccessibleTextRole:
        return 'Qt.AccessibleTextRole'
    elif role == 12 and role == Qt.AccessibleDescriptionRole:
        return 'Qt.AccessibleDescriptionRole'
    elif role == 13 and role == Qt.SizeHintRole:
        return 'Qt.SizeHintRole'
    elif role == 14 and role == Qt.InitialSortOrderRole:
        return 'Qt.InitialSortOrderRole'
    elif role == 32 and role == Qt.UserRole:
        return 'Qt.UserRole'

    return 'Unknown Role (Role Number Change?): ' + str(role)


def seconds_to_hh_mm_ss(seconds: int) -> List[int]:
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_MINUTE = 60

    hh = seconds // SECONDS_PER_HOUR
    mm = seconds % SECONDS_PER_HOUR // SECONDS_PER_MINUTE
    ss = seconds % SECONDS_PER_MINUTE

    return [hh, mm, ss]


def seconds_to_str(seconds: int) -> str:
    hh, mm, ss = seconds_to_hh_mm_ss(seconds)

    return f'{hh: >2d}:{mm:0>2d}:{ss:0>2d}'


def timedelta2str(delta: datetime.timedelta) -> str:
    return seconds_to_str(int(delta.total_seconds()))

def period_to_str(prd: pendulum.Period) -> str:
    return seconds_to_str(prd.seconds)

def pendulum2str(pnd: pendulum.DateTime) -> str:

    t = pnd.time()

    hh, mm, ss = t.hour, t.minute, t.second

    return f'{hh: >2d}:{mm:0>2d}:{ss:0>2d}'


def logged(logger=logging.getLogger('tslot-main'), disabled=True):
    """
    Create a configured decorator that controls logging output of a function

    :param logger: the logger to send output to
    :param disabled: True if the logger should be disabled, False otherwise
    """

    def logged_decorator(foo):
        """
        Decorate a function and surround its call with enter/leave logs

        Produce logging output of the form:
        > enter foo
          ...
        > leave foo (returned value)
        """

        @wraps(foo)
        def wrapper(*args, **kwargs):

            was_disabled = logger.disabled

            logger.disabled = disabled

            logger.debug(f'enter {foo.__qualname__}')

            result = foo(*args, **kwargs)

            logger.debug(f'leave {foo.__qualname__} ({result})')

            logger.disabled = was_disabled

            return result

        return wrapper

    return logged_decorator


def configure_logging():
    """Set up loggers/handlers/formatters as well as their logging levels"""

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(asctime)22s %(levelname)7s %(module)20s %(process)6d %(thread)15d %(message)s'
            }
            , 'simple': {
                'format': '%(levelname)s %(message)s'
            }
        }
        , 'handlers': {
            'console-main': {
                'level': 'DEBUG'
                , 'class': 'logging.StreamHandler'
                , 'formatter': 'verbose'
            }
            , 'console-data': {
                'level': 'DEBUG'
                , 'class': 'logging.StreamHandler'
                , 'formatter': 'verbose'
            }
            , 'file': {
                'level': 'DEBUG'
                , 'class': 'logging.handlers.RotatingFileHandler'
                , 'formatter': 'verbose'
                , 'filename': 'tslot.log'
                , 'maxBytes': 10485760 # 10 MiB
                , 'backupCount': 3
            }
        },
        'loggers': {
            'tslot-main': {
                'handlers': ['console-main', 'file']
                , 'level': 'DEBUG'
            }
            , 'tslot-data': {
                'handlers': ['console-data']
                , 'level': 'DEBUG'
            }
        }
    })

    # The reason there are two loggers is because there is the gui (main) thread
    # and a database (data) thread. If both threads use the same logger, it all
    # becomes messy quite quickly (messages go missing or pop up when disabled)
    logger = logging.getLogger('tslot-main')
    logger.debug('tslot-main logger is online')

    logger = logging.getLogger('tslot-data')
    logger.debug('tslot-data logger is online')
