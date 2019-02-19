import re

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QColor

from src.common.sip_singleton import SipSingleton
from src.client.srv_color.model.color import TColorModel


class TColorService(QObject, metaclass=SipSingleton):

    bg_color_fst_changed = pyqtSignal()
    bg_color_fst_lgt_changed = pyqtSignal()
    bg_color_fst_drk_changed = pyqtSignal()

    bg_color_snd_changed = pyqtSignal()
    bg_color_snd_lgt_changed = pyqtSignal()
    bg_color_snd_drk_changed = pyqtSignal()

    bg_color_err_changed = pyqtSignal()
    bg_color_err_lgt_changed = pyqtSignal()
    bg_color_err_drk_changed = pyqtSignal()

    fg_color_fst_changed = pyqtSignal()
    fg_color_fst_lgt_changed = pyqtSignal()
    fg_color_fst_drk_changed = pyqtSignal()

    fg_color_snd_changed = pyqtSignal()
    fg_color_snd_lgt_changed = pyqtSignal()
    fg_color_snd_drk_changed = pyqtSignal()

    fg_color_err_changed = pyqtSignal()
    fg_color_err_lgt_changed = pyqtSignal()
    fg_color_err_drk_changed = pyqtSignal()

    def __init__(self, parent: QObject = None):

        super().__init__(parent)

        self.kickstarted = False

        self.colors = TColorModel()

        # aka primary color
        self.bg_color_fst = self.colors.color_gray_500
        self.bg_color_fst_lgt = self.colors.color_gray_100
        self.bg_color_fst_drk = self.colors.color_gray_700
        # aka secondary color
        self.bg_color_snd = self.colors.color_cyan_500
        self.bg_color_snd_lgt = self.colors.color_cyan_100
        self.bg_color_snd_drk = self.colors.color_cyan_700
        # aka warning/error color
        self.bg_color_err = self.colors.color_red_500
        self.bg_color_err_lgt = self.colors.color_red_700
        self.bg_color_err_drk = self.colors.color_red_100
        # aka on primary color
        self.fg_color_fst = self.colors.color_black
        self.fg_color_fst_lgt = self.colors.color_black
        self.fg_color_fst_drk = self.colors.color_white
        # aka on secondary color
        self.fg_color_snd = self.colors.color_black
        self.fg_color_snd_lgt = self.colors.color_black
        self.fg_color_snd_drk = self.colors.color_white
        # aka on warning/error color
        self.fg_color_err = self.colors.color_white
        self.fg_color_err_lgt = self.colors.color_black
        self.fg_color_err_drk = self.colors.color_white

        self.color_pattern = re.compile("^(fg|bg)_color_(fst|snd|err)(|_lgt|_drk)$")

        self.kickstarted = True

    def is_color_attr(self, key) -> bool:
        return self.color_pattern.match(key)

    def __setattr__(self, key, val):

        super().__setattr__(key, val)

        if not self.kickstarted:
            # This object is being initialized, __init__ is setting some attributes.
            # Signal handlers might expect the service to be fully initialized, so avoid
            # triggering the signals for now.
            return

        if self.is_color_attr(key):
            self.__getattribute__(key + "_changed").emit()

    def to_qt(self, hex_color: str, alpha: int = 255) -> QColor:
        if hex_color.startswith("#"):
            hex_color = hex_color[1:]
        if len(hex_color) != 6:
            raise RuntimeError("Expected six hexadecimal digits")

        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)

        return QColor(r, g, b, alpha)
