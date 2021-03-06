import time

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QFontDatabase

from src.client.common.widget.common.font_aware_widget import TFontAwareWidget
from src.client.common.widget.line_edit.color_aware_line_edit import \
    TAlternateColorAwareLineEdit
from src.common.logger import logged, logmain


class TTimerLineEdit(TAlternateColorAwareLineEdit, TFontAwareWidget):

    @logged(logger=logmain, disabled=True)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setup_font()
        self.setPlaceholderText('Type task/project')

        self._font_service.base_height_changed.connect(
            self._handle_base_height_changed
        )

    @logged(logger=logmain, disabled=True)
    def _handle_font_loaded(self):
        self.setup_font()

    def _handle_base_height_changed(self):
        self.updateGeometry()

    @logged(logger=logmain, disabled=True)
    def setup_font(self):
        self.setFont(
            QFontDatabase().font('Quicksand', 'Bold', self._font_service.font_serif_size)
        )

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
