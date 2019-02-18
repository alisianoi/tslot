from typing import Tuple

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QValidator
from PyQt5.QtWidgets import QLineEdit, QSizePolicy, QWidget

from logger import logged, logger
from srv_font.service.font import FontService


class MyLineEditValidator(QValidator):

    def __init__(self, parent: QWidget = None):

        super().__init__(parent)

    @logged(disabled=True)
    def validate(self, txt: str, pos: int) -> Tuple[QValidator.State, str, int]:

        if not txt.startswith("#"):
            return (QValidator.Invalid, txt, pos)

        if len(txt) > 7:
            return (QValidator.Invalid, txt, pos)

        for item in txt[1:]:
            lower = item.lower()

            if lower < '0' or lower > 'f':
                return (QValidator.Invalid, txt, pos)

        if len(txt) == 7:
            return (QValidator.Acceptable, txt, pos)

        return (QValidator.Intermediate, txt, pos)


class MyLineEdit(QLineEdit):

    def __init__(self, parent: QWidget = None):

        super().__init__(parent)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.validator = MyLineEditValidator(self)
        self.setValidator(self.validator)

    def sizeHint(self):
        size_hint = super().sizeHint()
        return QSize(size_hint.width(), FontService().base_height)
