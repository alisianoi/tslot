import logging.config

from functools import wraps
from PyQt5.QtCore import *


def orient2str(orientation: Qt.Orientation):
    if orientation == 0x1 and orientation == Qt.Horizontal:
        return 'Qt.Horizontal'
    elif orientation == 0x2 and orientation == Qt.Vertical:
        return 'Qt.Vertical'

    return 'Unknown Orientation (Orientation Number Change?): ' + str(orientation)

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


def logged(foo, logger=logging.getLogger('tslot')):
    '''
    Decorate a function and surround its call with enter/leave logs

    Produces logging output of the form:
    > enter foo
      ...
    > leave foo (returned value)
    '''

    @wraps(foo)
    def wrapper(*args, **kwargs):
        logger.debug(f'enter {foo.__qualname__}')

        result = foo(*args, **kwargs)

        logger.debug(f'leave {foo.__qualname__} ({result})')

        return result

    return wrapper


def configure_logging():
    '''
    Set up loggers/handlers/formatters as well as their logging levels
    '''

    logging.config.dictConfig({
        'version': 1,
        'formatters': {
            'verbose': {
                'format': '%(asctime)22s %(levelname)7s %(module)10s %(process)6d %(thread)15d %(message)s'
            }
            , 'simple': {
                'format': '%(levelname)s %(message)s'
            }
        }
        , 'handlers': {
            'file': {
                'level': 'DEBUG'
                , 'class': 'logging.handlers.RotatingFileHandler'
                , 'formatter': 'verbose'
                , 'filename': 'tslot.log'
                , 'maxBytes': 10485760 # 10 MiB
                , 'backupCount': 3
            }
            , 'console': {
                'level': 'DEBUG'
                , 'class': 'logging.StreamHandler'
                , 'formatter': 'verbose'
            }
        },
        'loggers': {
            'tslot': {
                'handlers': ['console', 'file']
                , 'level': 'DEBUG',
            }
        }
    })

    logger = logging.getLogger('tslot')
    logger.debug('tslot logger is online')
