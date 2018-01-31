import logging

from pathlib import Path

from PyQt5.QtGui import *


def initialize_font_databse(path: Path=None):
    '''
    Add custom fonts into the Qt's system font database

    The database itself is a singleton and a thread-safe class, so you
    coule initialize/update it at any point and then use anywhere.
    '''
    
    logger = logging.getLogger('tslot')
    logger.debug('initialize_font_database has a logger')

    database = QFontDatabase()

    if path is None:
        path = Path(Path.cwd(), Path('font'))
        logger.debug(f'Will use default font path {path}')

    if not path.exists():
        logger.debug(f'Path {path} does not exist')

        return

    must_visit = [path]

    while must_visit:
        path = must_visit.pop()

        logger.debug(f'Will try {path}')

        for entry in path.iterdir():

            if entry.name.endswith('.ttf'):
                logger.debug(f'Add font from {entry}')
                database.addApplicationFont(str(entry))
            elif entry.is_dir():
                must_visit.append(entry)
