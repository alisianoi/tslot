import logging, logging.config

from functools import wraps


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
logmain = logging.getLogger('tslot-main')
logmain.debug('tslot-main logger is online')

logdata = logging.getLogger('tslot-data')
logdata.debug('tslot-data logger is online')
