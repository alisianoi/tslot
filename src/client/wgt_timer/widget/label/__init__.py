from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtWidgets import QLabel

from src.client.common.widget.label.animated_label import *
from src.client.common.widget.label.color_aware_label import *
from src.client.common.widget.label.font_aware_label import *


class TTimerLabel(TFontAwareLabel, TPrimaryColorAwareLabel):

    TIMER_IS_ZERO = '00:00:00'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setContentsMargins(20, 0, 20, 0)
        self.setText(self.TIMER_IS_ZERO)
        self.setAlignment(Qt.AlignCenter)

        self.setup_font()
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def setup_font(self):
        self.setFont(
            QFontDatabase().font(
                'Inconsolata', 'Bold', 4 * self._font_service.font_monospace_size / 3
            )
        )
