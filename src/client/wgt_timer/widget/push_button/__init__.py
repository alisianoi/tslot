import time
from pathlib import Path

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from src.client.common.widget.push_button.color_aware_push_button import \
    TFailureColorAwarePushButton
from src.client.common.widget.push_button.font_aware_push_button import \
    TSquarePushButton
from src.client.srv_font.service.font import TFontService


class TIconAwarePushButton(TSquarePushButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._font_service = TFontService()

        path_svgs_solid = Path(
            self._font_service.default_font_path(), 'fontawesome', 'svgs', 'solid'
        )

        self.play_icon = QIcon(str(Path(path_svgs_solid, 'play.svg')))
        self.stop_icon = QIcon(str(Path(path_svgs_solid, 'stop.svg')))
        self.nuke_icon = QIcon(str(Path(path_svgs_solid, 'trash-alt.svg')))


class TTimerPushButton(TIconAwarePushButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.state = "play"

        self.setIcon(self.play_icon)

        self.clicked.connect(self._handle_clicked)

    @pyqtSlot(bool)
    def _handle_clicked(self, checked: bool):
        if self.state == "play":
            self.state = "stop"
            self.setIcon(self.nuke_icon)
        elif self.state == "stop":
            self.state = "play"
            self.setIcon(self.play_icon)
        else:
            raise RuntimeError("Failed to determine timer push button state")


class TTimerNukeButton(TIconAwarePushButton, TFailureColorAwarePushButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setIcon(self.nuke_icon)
