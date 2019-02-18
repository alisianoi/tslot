import re
from pathlib import Path
from threading import Thread

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QFont

from common.sip_singleton import SipSingleton
from logger import logged, logger


class TFontService(QObject, metaclass=SipSingleton):

    base_height_changed = pyqtSignal()

    font_serif_changed = pyqtSignal()
    font_sans_serif_changed = pyqtSignal()
    font_monospace_changed = pyqtSignal()

    def __init__(self, parent: QObject = None):

        super().__init__(parent)

        self.kickstarted = False

        self.font_size = 12
        self.base_height = 32

        self.font_serif_name = 'Serif'
        self.font_sans_serif_name = 'Sans Serif'
        self.font_monospace_name = 'Monospace'

        self.font_serif_size = self.font_size
        self.font_sans_serif_size = self.font_size
        self.font_monospace_size = self.font_size

        self.font_serif_style_name = 'Normal'
        self.font_sans_serif_style_name = 'Normal'
        self.font_monospace_style_name = 'Normal'

        # Assign font as last step because that triggeres a signal
        font = QFont(self.font_serif_name, self.font_serif_size)
        font.setStyleName(self.font_serif_style_name)
        self.font_serif = font

        font = QFont(self.font_sans_serif_name, self.font_sans_serif_size)
        font.setStyleName(self.font_sans_serif_style_name)
        self.font_sans_serif = font

        font = QFont(self.font_monospace_name, self.font_monospace_size)
        font.setStyleName(self.font_monospace_style_name)
        self.font_monospace = font

        self.kickstarted = True

    def __setattr__(self, key, val):
        super().__setattr__(key, val)

        if key == "base_height":
            self.base_height_changed.emit()
        elif key == "font_serif":
            self.font_serif_changed.emit()
        elif key == "font_sans_serif":
            self.font_sans_serif_changed.emit()
        elif key == "font_monospace":
            self.font_monospace_changed.emit()
        elif key == "font_serif_name" \
            or key == "font_serif_size" \
            or key == "font_serif_style_name":
            self._change_font("font_serif")
        elif key == "font_sans_serif_name" \
            or key == "font_sans_serif_size" \
            or key == "font_sans_serif_style_name":
            self._change_font("font_sans_serif")
        elif key == "font_monospace_name" \
            or key == "font_monospace_size" \
            or key == "font_monospace_style_name":
            self._change_font("font_monospace")

    def _change_font(self, font_prefix: str):
        try:
            font_name = getattr(self, font_prefix + "_name")
            font_size = getattr(self, font_prefix + "_size")
            font_style_name = getattr(self, font_prefix + "_style_name")

            font = QFont(font_name, font_size)
            font.setStyleName(font_style_name)

            setattr(self, font_prefix, font)
        except AttributeError:
            if not self.kickstarted:
                # the instance has not finished initializing yet, suppress
                return
            # the instance has been fully initialized, something else is wrong
            raise
