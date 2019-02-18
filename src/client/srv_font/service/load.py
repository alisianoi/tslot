from pathlib import Path
from threading import Thread

from PyQt5.QtGui import QFontDatabase

from logger import logged, logger


class FontLoader(Thread):
    """
    Add custom fonts into the Qt's system font database

    The database itself is a singleton and a thread-safe class, so you
    could initialize/update it at any point and then use anywhere.
    """

    def __init__(self, path: Path = None):
        super().__init__()

        self.path = path

    @logged(disabled=False)
    def run(self):

        font_database = QFontDatabase()

        if self.path is None:
            self.path = Path(Path.cwd(), 'asset')

        if not self.path.exists():
            logger.warning('FontLoader cannot find asset folder')

            return

        msg = 'Font {} is in application font db with id {}'

        must_visit = [self.path]

        while must_visit:
            path = must_visit.pop()

            for entry in path.iterdir():
                name = str(entry)

                if entry.name.endswith('.ttf'):
                    font_id = font_database.addApplicationFont(name)
                    logger.debug(msg.format(name, font_id))
                elif entry.name.endswith('.otf'):
                    font_id = font_database.addApplicationFont(name)
                    logger.debug(msg.format(name, font_id))
                elif entry.is_dir():
                    must_visit.append(entry)
