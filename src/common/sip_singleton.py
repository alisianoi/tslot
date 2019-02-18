import sip

from logger import logger


class SipSingleton(sip.wrappertype):

    instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in SipSingleton.instances:
            logger.debug(f'Will create an instance of {cls}')
            SipSingleton.instances[cls] = super().__call__(*args, *kwargs)

        return SipSingleton.instances[cls]
