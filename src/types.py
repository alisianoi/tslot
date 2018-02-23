import logging

from src.db.model import DateModel, TaskModel, SlotModel


class LoadFailed(Exception):

    def __init__(self, message):

        super().__init__()

        self.logger = logging.getLogger('tslot')
        self.logger.warning('Emitting a LoadFailed:')
        self.logger.warning(message)

        self.message = message
