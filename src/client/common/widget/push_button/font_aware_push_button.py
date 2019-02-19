from PyQt5.QtWidgets import QPushButton

from src.client.srv_font.service.font import TFontService


class TFontAwarePushButton(QPushButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._font_service = TFontService()


class TSquarePushButton(TFontAwarePushButton):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setFixedWidth(2 * self._font_service.base_height)
        self.setFixedHeight(2 * self._font_service.base_height)
