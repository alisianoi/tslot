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

    if not path.exists():
        return

    must_visit = [path]

    while must_visit:
        path = must_visit.pop()

        for entry in path.iterdir():
            if entry.name.endswith('.ttf'):
                database.addApplicationFont(str(entry))
            elif entry.is_dir():
                must_visit.append(entry)
