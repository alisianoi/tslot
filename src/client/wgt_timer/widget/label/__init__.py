from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from src.client.common.widget.label.animated_label import TAnimatedLabel
from src.client.common.widget.label.color_aware_label import TPrimaryColorAwareLabel
from src.client.common.widget.label.font_aware_label import TFontAwareLabel


class TTimerLabel(TAnimatedLabel, TFontAwareLabel, TPrimaryColorAwareLabel):

    TIMER_IS_ZERO = '00:00:00'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setAlignment(Qt.AlignCenter)
        self.setText(self.TIMER_IS_ZERO)
