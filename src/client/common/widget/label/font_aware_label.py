from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel, QSizePolicy

from src.client.srv_font.service.font import TFontService
from src.common.logger import logged


class TFontAwareLabel(QLabel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._font_service = TFontService()

        self._font_service.base_height_changed.connect(
            self.handle_base_height_changed
        )
        self._font_service.font_sans_serif_changed.connect(
            self.handle_font_sans_serif_changed
        )

        self.setFont(self._font_service.font_sans_serif)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

    def handle_base_height_changed(self):
        self.updateGeometry()

    def handle_font_sans_serif_changed(self):
        self.setFont(self._font_service.font_sans_serif)
        self.updateGeometry()

    @logged(disabled=True)
    def sizeHint(self) -> QSize:
        size_hint = super().sizeHint()
        return QSize(size_hint.width(), 2 * self._font_service.base_height)

    @logged(disabled=True)
    def minimumSizeHint(self) -> QSize:
        size_hint = super().sizeHint()
        return QSize(size_hint.width(), 2 * self._font_service.base_height)

    @logged(disabled=True)
    def maximumSizeHint(self) -> QSize:
        size_hint = super().maximumSizeHint()
        return QSize(size_hint.width(), 2 * self._font_service.base_height)
