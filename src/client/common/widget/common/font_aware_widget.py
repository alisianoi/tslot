from PyQt5.QtWidgets import QWidget

from src.client.srv_font.service.font import TFontService


class TFontAwareWidget(QWidget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._font_service = TFontService()
        self._font_service.font_loaded.connect(self._handle_font_loaded)

    def _handle_font_loaded(self):
        raise NotImplementedError("Failed to handle newly loaded font")
