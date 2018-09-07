import logging

from pathlib import Path
from PyQt5.QtCore import QObject


class Stylist(QObject):
    """Load and store files that contain Qt Style Sheets"""

    def __init__(self, path: Path=None, parent: QObject=None):

        super().__init__(parent)

        self.logger = logging.getLogger('tslot')

        self.styles = {}

        if path is None:
            path = Path(Path.cwd(), Path('css'), Path('tslot.css'))

        if not path.exists():
            self.logger.debug(f'Could not find {path.name} in {path}')

            return

        with open(path) as src:
            self.styles['tslot'] = src.read()
